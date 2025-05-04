from typing import Dict, List, Optional
from datetime import datetime
from models import AssessmentSession, AssessmentAnswer
from sqlalchemy.orm import Session

class AssessmentManager:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.assessments = {
            "PHQ-9": {
                "title": "PHQ-9 抑郁筛查量表",
                "description": "PHQ-9是一个用于筛查、诊断和监测抑郁症状的9项量表。",
                "questions": [
                    {
                        "id": 1,
                        "text": "做事时提不起劲或没有兴趣",
                        "options": [
                            {"value": 0, "text": "完全不会"},
                            {"value": 1, "text": "几天"},
                            {"value": 2, "text": "一半以上的天数"},
                            {"value": 3, "text": "几乎每天"}
                        ]
                    },
                    {
                        "id": 2,
                        "text": "感到心情低落、沮丧或绝望",
                        "options": [
                            {"value": 0, "text": "完全不会"},
                            {"value": 1, "text": "几天"},
                            {"value": 2, "text": "一半以上的天数"},
                            {"value": 3, "text": "几乎每天"}
                        ]
                    },
                    {
                        "id": 3,
                        "text": "入睡困难、睡不安稳或睡得太多",
                        "options": [
                            {"value": 0, "text": "完全不会"},
                            {"value": 1, "text": "几天"},
                            {"value": 2, "text": "一半以上的天数"},
                            {"value": 3, "text": "几乎每天"}
                        ]
                    },
                    {
                        "id": 4,
                        "text": "感到疲倦或没有活力",
                        "options": [
                            {"value": 0, "text": "完全不会"},
                            {"value": 1, "text": "几天"},
                            {"value": 2, "text": "一半以上的天数"},
                            {"value": 3, "text": "几乎每天"}
                        ]
                    },
                    {
                        "id": 5,
                        "text": "食欲不振或吃太多",
                        "options": [
                            {"value": 0, "text": "完全不会"},
                            {"value": 1, "text": "几天"},
                            {"value": 2, "text": "一半以上的天数"},
                            {"value": 3, "text": "几乎每天"}
                        ]
                    },
                    {
                        "id": 6,
                        "text": "觉得自己很糟或觉得自己很失败，或让自己或家人失望",
                        "options": [
                            {"value": 0, "text": "完全不会"},
                            {"value": 1, "text": "几天"},
                            {"value": 2, "text": "一半以上的天数"},
                            {"value": 3, "text": "几乎每天"}
                        ]
                    },
                    {
                        "id": 7,
                        "text": "对事物专注有困难，例如阅读报纸或看电视时",
                        "options": [
                            {"value": 0, "text": "完全不会"},
                            {"value": 1, "text": "几天"},
                            {"value": 2, "text": "一半以上的天数"},
                            {"value": 3, "text": "几乎每天"}
                        ]
                    },
                    {
                        "id": 8,
                        "text": "行动或说话速度缓慢到别人已经察觉？或正好相反，变得比平日更烦躁或坐立不安、动来动去",
                        "options": [
                            {"value": 0, "text": "完全不会"},
                            {"value": 1, "text": "几天"},
                            {"value": 2, "text": "一半以上的天数"},
                            {"value": 3, "text": "几乎每天"}
                        ]
                    },
                    {
                        "id": 9,
                        "text": "有不如死掉或用某种方式伤害自己的念头",
                        "options": [
                            {"value": 0, "text": "完全不会"},
                            {"value": 1, "text": "几天"},
                            {"value": 2, "text": "一半以上的天数"},
                            {"value": 3, "text": "几乎每天"}
                        ]
                    }
                ],
                "scoring": {
                    "ranges": [
                        {"min": 0, "max": 4, "level": "无抑郁", "description": "您的抑郁症状很轻微，建议继续保持良好的生活习惯。"},
                        {"min": 5, "max": 9, "level": "轻度抑郁", "description": "您可能有轻度抑郁症状，建议适当调整作息，保持运动，必要时寻求专业帮助。"},
                        {"min": 10, "max": 14, "level": "中度抑郁", "description": "您可能有中度抑郁症状，建议及时寻求专业心理咨询或医疗帮助。"},
                        {"min": 15, "max": 19, "level": "中重度抑郁", "description": "您可能有中重度抑郁症状，建议尽快寻求专业医疗帮助。"},
                        {"min": 20, "max": 27, "level": "重度抑郁", "description": "您可能有重度抑郁症状，建议立即寻求专业医疗帮助。"}
                    ],
                    "suicide_risk": {
                        "threshold": 1,
                        "warning": "如果您对第9题的回答是'几天'或以上，建议立即寻求专业医疗帮助。"
                    }
                }
            }
        }

    def get_assessment_info(self, assessment_type: str) -> Optional[Dict]:
        """获取评估信息"""
        return self.assessments.get(assessment_type)

    def create_assessment_session(self, session_id: str, assessment_type: str) -> AssessmentSession:
        """创建新的评估会话"""
        assessment_session = AssessmentSession(
            session_id=session_id,
            assessment_type=assessment_type,
            status="in_progress"
        )
        self.session_manager.db.add(assessment_session)
        self.session_manager.db.commit()
        return assessment_session

    def add_answer(self, session_id: str, question_id: int, answer: int) -> AssessmentAnswer:
        """添加评估答案"""
        assessment_session = self.session_manager.db.query(AssessmentSession)\
            .filter(AssessmentSession.session_id == session_id)\
            .first()
            
        if not assessment_session:
            raise ValueError("评估会话不存在")
            
        assessment_answer = AssessmentAnswer(
            assessment_session_id=assessment_session.id,
            question_id=question_id,
            answer=answer
        )
        self.session_manager.db.add(assessment_answer)
        self.session_manager.db.commit()
        return assessment_answer

    def get_assessment_answers(self, session_id: str) -> List[AssessmentAnswer]:
        """获取评估答案"""
        assessment_session = self.session_manager.db.query(AssessmentSession)\
            .filter(AssessmentSession.session_id == session_id)\
            .first()
            
        if not assessment_session:
            raise ValueError("评估会话不存在")
            
        return self.session_manager.db.query(AssessmentAnswer)\
            .filter(AssessmentAnswer.assessment_session_id == assessment_session.id)\
            .order_by(AssessmentAnswer.question_id)\
            .all()

    def complete_assessment(self, session_id: str) -> AssessmentSession:
        """完成评估"""
        assessment_session = self.session_manager.db.query(AssessmentSession)\
            .filter(AssessmentSession.session_id == session_id)\
            .first()
            
        if not assessment_session:
            raise ValueError("评估会话不存在")
            
        # 计算总分
        answers = self.get_assessment_answers(session_id)
        total_score = sum(answer.answer for answer in answers)
        
        # 获取评估信息
        assessment_info = self.get_assessment_info(assessment_session.assessment_type)
        if not assessment_info:
            raise ValueError("评估类型不存在")
            
        # 确定评估结果
        interpretation = None
        for range_info in assessment_info["scoring"]["ranges"]:
            if range_info["min"] <= total_score <= range_info["max"]:
                interpretation = {
                    "level": range_info["level"],
                    "description": range_info["description"]
                }
                break
                
        # 检查自杀风险
        suicide_risk = None
        if assessment_session.assessment_type == "PHQ-9":
            question_9_answer = next(
                (answer.answer for answer in answers if answer.question_id == 9),
                None
            )
            if question_9_answer and question_9_answer >= assessment_info["scoring"]["suicide_risk"]["threshold"]:
                suicide_risk = assessment_info["scoring"]["suicide_risk"]["warning"]
        
        # 更新评估会话
        assessment_session.status = "completed"
        assessment_session.completed_at = datetime.utcnow()
        assessment_session.total_score = total_score
        assessment_session.interpretation = {
            "score": total_score,
            "interpretation": interpretation,
            "suicide_risk": suicide_risk
        }
        
        self.session_manager.db.commit()
        return assessment_session

    def get_assessment_result(self, session_id: str) -> Dict:
        """获取评估结果"""
        assessment_session = self.session_manager.db.query(AssessmentSession)\
            .filter(AssessmentSession.session_id == session_id)\
            .first()
            
        if not assessment_session:
            raise ValueError("评估会话不存在")
            
        if assessment_session.status != "completed":
            raise ValueError("评估尚未完成")
            
        return assessment_session.interpretation 