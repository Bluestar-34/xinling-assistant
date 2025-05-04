from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import requests
import uuid
from typing import Optional
from database import get_db, SessionManager
from models import Base, engine
from context_manager import ContextManager
import json

# 加载环境变量（从根目录加载）
load_dotenv(dotenv_path='.env')

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API配置
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN 未设置！请在根目录的.env文件中设置API_TOKEN")

# 创建数据库会话管理器
db = next(get_db())
session_manager = SessionManager(db)
context_manager = ContextManager(session_manager)

# 系统提示词
SYSTEM_PROMPT = """你是一位专业的心理咨询师，名叫小南心。你的职责是：
1. 以温暖、专业的态度倾听和回应用户
2. 运用同理心理解用户的感受
3. 提供具有建设性的建议和支持
4. 保持对话的连贯性和专注度
5. 在必要时引导用户寻求专业帮助

请记住：
- 始终保持耐心和理解
- 避免做出诊断或医疗建议
- 在用户分享困扰时给予情感支持
- 使用清晰、易懂的语言
- 保持对话的专业性和边界感"""

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "message": "你好",
                "session_id": None
            }
        }

class ChatResponse(BaseModel):
    response: str
    session_id: str
    context_info: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "response": "你好！我是小南心，很高兴见到你。",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "context_info": {
                    "message_count": 1,
                    "duration": "0:00:01",
                    "user_info": {}
                }
            }
        }

def get_ai_response(message: str, context: list = None) -> str:
    """获取AI回复"""
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # 添加上下文消息
        if context:
            messages.extend(context)
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": "Qwen/QwQ-32B",
            "messages": messages,
            "stream": False,
            "max_tokens": 512,
            "enable_thinking": False,
            "thinking_budget": 512,
            "min_p": 0.05,
            "stop": None,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"}
        }

        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }

        # 打印详细的调试信息
        print("\n=== API请求详情 ===")
        print(f"URL: {API_URL}")
        print(f"Headers: {json.dumps(headers, ensure_ascii=False)}")
        print(f"Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        print("==================\n")

        # 使用requests.request方法发送请求
        response = requests.request(
            "POST", 
            API_URL, 
            json=payload, 
            headers=headers, 
            timeout=30,
            verify=True  # 确保SSL验证
        )
        
        # 打印响应信息
        print("\n=== API响应详情 ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        print("==================\n")
        
        # 检查响应状态
        if response.status_code != 200:
            error_msg = f"API请求失败: 状态码 {response.status_code}, 响应内容: {response.text}"
            print(error_msg)
            return "抱歉，服务暂时不可用，请稍后再试。"
            
        result = response.json()
        
        # 验证响应格式
        if not result.get("choices") or not result["choices"][0].get("message"):
            print(f"无效的API响应格式: {result}")
            return "抱歉，服务响应格式有误，请稍后再试。"
            
        return result["choices"][0]["message"]["content"]
        
    except requests.exceptions.Timeout:
        print("请求超时")
        return "抱歉，响应时间有点长。请再说一遍您的问题，我会仔细聆听。"
    except requests.exceptions.RequestException as e:
        print(f"API请求错误: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"错误状态码: {e.response.status_code}")
            print(f"错误响应头: {dict(e.response.headers)}")
            print(f"错误响应体: {e.response.text}")
        return "非常抱歉，我现在可能无法正常回应。请稍后再试。"
    except Exception as e:
        print(f"处理错误: {str(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")
        return "抱歉，我需要一点时间来思考。请您重新表达一下。"

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # 处理会话ID
        session_id = request.session_id or str(uuid.uuid4())
        if not session_manager.get_session(session_id):
            session_manager.create_session(session_id)

        # 获取对话上下文
        context = context_manager.get_context(session_id)
        
        # 记录用户消息
        context_manager.add_message(session_id, "user", request.message)
        
        # 获取AI回复
        assistant_message = get_ai_response(request.message, context)
        
        # 记录AI回复
        context_manager.add_message(session_id, "assistant", assistant_message)
        
        # 获取会话统计
        session_stats = context_manager.get_session_summary(session_id)
        
        return ChatResponse(
            response=assistant_message,
            session_id=session_id,
            context_info=session_stats
        )
        
    except Exception as e:
        print(f"处理错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """获取会话信息"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
        
    session_stats = context_manager.get_session_summary(session_id)
    return {
        "session_id": session_id,
        "created_at": session.created_at,
        "stats": session_stats
    }

@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """删除会话"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
        
    context_manager.cleanup_context(session_id)
    session_manager.delete_session(session_id)
    return {"message": "会话已删除"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 