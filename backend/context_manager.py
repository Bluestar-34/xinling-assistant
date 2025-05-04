from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from database import SessionManager
from models import Message
import json

class ContextManager:
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.max_tokens = 4000
        self.max_messages = 20  # 最大消息数量
        self.context_window = 10  # 上下文窗口大小
        self.summary_threshold = 20  # 触发总结的消息数量阈值
        self.user_info = {}  # 存储用户信息
        self.max_history = 20  # 最大历史消息数
        self.max_age = timedelta(hours=24)  # 会话最大保存时间
        
        # 系统提示词
        self.system_prompt = """你是一个专业的心理咨询师，名叫小南心。你需要：
1. 保持温和、专业的语气
2. 认真倾听并理解用户的问题
3. 记住用户提供的重要信息
4. 避免重复询问已知信息
5. 在回答时考虑上下文，保持对话的连贯性
6. 适时总结对话要点，确保理解准确
7. 对用户的情感给予适当的回应和支持"""

    def get_context(self, session_id: str) -> List[Dict[str, str]]:
        """获取对话上下文，包含压缩和总结功能"""
        messages = self.session_manager.get_messages(session_id)
        if not messages:
            return [{"role": "system", "content": self.system_prompt}]

        # 如果消息数量超过阈值，生成总结
        if len(messages) > self.summary_threshold:
            summary = self._generate_summary(messages[:-self.context_window])
            context = [{"role": "system", "content": self.system_prompt}]
            context.append({"role": "system", "content": f"之前的对话总结：{summary}"})
            context.extend([{"role": msg.role, "content": msg.content} for msg in messages[-self.context_window:]])
        else:
            context = [{"role": "system", "content": self.system_prompt}]
            context.extend([{"role": msg.role, "content": msg.content} for msg in messages])

        # 添加用户信息到上下文
        if session_id in self.user_info:
            user_info = self.user_info[session_id]
            context.append({
                "role": "system",
                "content": f"用户信息：{json.dumps(user_info, ensure_ascii=False)}"
            })

        return context

    def _generate_summary(self, messages: List[Message]) -> str:
        """生成对话总结"""
        if not messages:
            return ""

        # 提取关键信息
        key_points = []
        current_topic = None
        topic_messages = []
        
        for msg in messages:
            if msg.role == "user":
                # 提取用户信息
                self._extract_user_info(msg.session_id, msg.content)
                
                # 分析话题
                if not current_topic:
                    current_topic = msg.content
                    topic_messages = [msg]
                else:
                    # 如果新消息与当前话题相关，添加到当前话题
                    if self._is_related_topic(current_topic, msg.content):
                        topic_messages.append(msg)
                    else:
                        # 总结当前话题并开始新话题
                        key_points.append(self._summarize_topic(topic_messages))
                        current_topic = msg.content
                        topic_messages = [msg]
            else:
                if topic_messages:
                    topic_messages.append(msg)
        
        # 处理最后一个话题
        if topic_messages:
            key_points.append(self._summarize_topic(topic_messages))

        # 生成总结
        summary = "之前的对话要点：\n" + "\n".join(key_points[-5:])  # 只保留最近5个要点
        return summary

    def _is_related_topic(self, topic: str, message: str) -> bool:
        """判断消息是否与当前话题相关"""
        # 这里可以实现更复杂的话题相关性判断逻辑
        # 目前使用简单的关键词匹配
        topic_keywords = set(topic.lower().split())
        message_keywords = set(message.lower().split())
        return len(topic_keywords.intersection(message_keywords)) > 0

    def _summarize_topic(self, messages: List[Message]) -> str:
        """总结单个话题的对话"""
        if not messages:
            return ""
            
        user_messages = [msg.content for msg in messages if msg.role == "user"]
        assistant_messages = [msg.content for msg in messages if msg.role == "assistant"]
        
        summary = []
        if user_messages:
            summary.append(f"用户关注：{user_messages[0]}")
        if assistant_messages:
            summary.append(f"咨询师回应：{assistant_messages[-1]}")
            
        return " | ".join(summary)

    def _extract_user_info(self, session_id: str, content: str) -> None:
        """从消息中提取用户信息"""
        if session_id not in self.user_info:
            self.user_info[session_id] = {}
            
        # 提取各种用户信息
        info_patterns = {
            "age": r"我今年(\d+)岁",
            "name": r"我叫([^，。,.]+)",
            "location": r"我在([^，。,.]+)",
            "occupation": r"我是([^，。,.]+)",
            "emotion": r"我感到([^，。,.]+)",
            "concern": r"我担心([^，。,.]+)"
        }
        
        for key, pattern in info_patterns.items():
            import re
            match = re.search(pattern, content)
            if match:
                self.user_info[session_id][key] = match.group(1)

    def add_message(self, session_id: str, role: str, content: str) -> None:
        """添加新消息并管理上下文"""
        # 添加消息到数据库
        self.session_manager.add_message(session_id, role, content)
        
        # 更新用户信息
        if role == "user":
            self._extract_user_info(session_id, content)
        
        # 检查是否需要压缩上下文
        messages = self.session_manager.get_messages(session_id)
        if len(messages) > self.max_messages:
            self._compress_context(session_id)

    def _compress_context(self, session_id: str) -> None:
        """压缩上下文，保留重要信息"""
        messages = self.session_manager.get_messages(session_id)
        if len(messages) <= self.max_messages:
            return

        # 生成总结
        summary = self._generate_summary(messages[:-self.context_window])
        
        # 保留最近的对话
        recent_messages = messages[-self.context_window:]
        
        # 清理旧消息
        self.session_manager.clear_messages(session_id)
        
        # 添加总结消息
        self.session_manager.add_message(session_id, "system", summary)
        
        # 重新添加最近的对话
        for msg in recent_messages:
            self.session_manager.add_message(session_id, msg.role, msg.content)

    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """获取会话统计信息"""
        messages = self.session_manager.get_messages(session_id)
        if not messages:
            return {
                "message_count": 0,
                "duration": "0:00:00",
                "user_info": {}
            }
            
        # 计算消息数量
        message_count = len(messages)
        
        # 计算会话持续时间
        first_message = min(messages, key=lambda x: x.created_at)
        last_message = max(messages, key=lambda x: x.created_at)
        duration = last_message.created_at - first_message.created_at
        
        # 提取用户信息（如果有）
        user_info = {}
        user_messages = [msg for msg in messages if msg.role == "user"]
        if user_messages:
            # 这里可以添加更多用户信息提取逻辑
            pass
            
        return {
            "message_count": message_count,
            "duration": str(duration),
            "user_info": user_info
        }

    def cleanup_old_sessions(self) -> None:
        """清理过期会话"""
        cutoff_time = datetime.utcnow() - self.max_age
        old_messages = self.session_manager.get_messages(session_id=None)\
            .filter(Message.created_at < cutoff_time)\
            .all()
            
        for message in old_messages:
            self.session_manager.clear_messages(message.session_id)
            
        self.session_manager.db.commit()

    def cleanup_context(self, session_id: str) -> None:
        """清理过期的上下文数据"""
        self.session_manager.cleanup_old_sessions()
        # 清理用户信息
        if session_id in self.user_info:
            del self.user_info[session_id]

    def get_session_summary(self, session_id: str) -> Optional[Dict]:
        """获取会话摘要"""
        messages = self.session_manager.get_messages(session_id)
        if not messages:
            return None
            
        # 生成更详细的摘要
        summary = self._generate_summary(messages)
        
        return {
            "session_id": session_id,
            "message_count": len(messages),
            "summary": summary,
            "last_message": messages[-1].content if messages else None,
            "created_at": messages[0].created_at if messages else None,
            "topics": self._extract_topics(messages),
            "user_info": self.user_info.get(session_id, {})
        }

    def merge_context(self, old_session_id: str, new_session_id: str) -> None:
        """合并两个会话的上下文"""
        old_messages = self.session_manager.get_messages(old_session_id)
        summary = self._generate_summary(old_messages)
        
        # 合并用户信息
        if old_session_id in self.user_info:
            self.user_info[new_session_id] = self.user_info[old_session_id]
        
        # 添加摘要作为系统消息
        self.session_manager.add_message(new_session_id, "system", 
            f"以下是之前对话的摘要：\n{summary}\n\n现在继续我们的对话：")
        
        # 添加最近的对话
        recent_messages = old_messages[-self.context_window:]
        for msg in recent_messages:
            self.session_manager.add_message(new_session_id, msg.role, msg.content)

    def _extract_topics(self, messages: List[Message]) -> List[str]:
        """提取对话中的主要话题"""
        topics = []
        current_topic = None
        
        for msg in messages:
            if msg.role == "user":
                if not current_topic or not self._is_related_topic(current_topic, msg.content):
                    current_topic = msg.content
                    topics.append(current_topic)
        
        return topics[-5:]  # 只返回最近5个话题

    def _analyze_emotions(self, messages: List[Message]) -> List[str]:
        """分析对话中的情感倾向"""
        emotions = []
        emotion_keywords = {
            "开心": ["开心", "高兴", "快乐", "喜悦"],
            "难过": ["难过", "伤心", "悲伤", "痛苦"],
            "焦虑": ["焦虑", "担心", "紧张", "害怕"],
            "愤怒": ["生气", "愤怒", "恼火", "不满"],
            "平静": ["平静", "放松", "安心", "舒适"]
        }
        
        for msg in messages:
            if msg.role == "user":
                for emotion, keywords in emotion_keywords.items():
                    if any(keyword in msg.content for keyword in keywords):
                        emotions.append(emotion)
                        break
        
        return emotions[-5:]  # 只返回最近5个情感 