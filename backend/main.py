from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import requests

# 加载环境变量
load_dotenv()

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API配置
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_TOKEN = os.getenv("API_TOKEN")  # 从环境变量获取token

class Message(BaseModel):
    content: str

@app.post("/api/chat")
async def chat(message: Message):
    try:
        # 构建请求数据
        payload = {
            "model": "Qwen/QwQ-32B",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的心理咨询师，请以温暖、专业的态度回应用户的问题。"
                },
                {
                    "role": "user",
                    "content": message.content
                }
            ],
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

        # 发送请求
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # 检查响应状态
        
        # 解析响应
        result = response.json()
        return {"response": result["choices"][0]["message"]["content"]}
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API请求错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 