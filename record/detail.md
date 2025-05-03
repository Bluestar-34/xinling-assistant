# 心聆助手项目详细说明文档

## 后端部分

### 1. 技术栈
- FastAPI: 现代、高性能的 Python Web 框架
- Uvicorn: ASGI 服务器，用于运行 FastAPI 应用
- Requests: HTTP 客户端库，用于调用大模型 API
- Python-dotenv: 环境变量管理
- Pydantic: 数据验证和设置管理

### 2. 项目结构
```
backend/
└── main.py          # 主程序入口
```

### 3. 核心功能实现

#### 3.1 API 配置
```python
# API配置
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_TOKEN = os.getenv("API_TOKEN")  # 从环境变量获取token
```
- 使用环境变量管理 API 密钥，提高安全性
- 支持通过 .env 文件配置

#### 3.2 消息模型
```python
class Message(BaseModel):
    content: str
```
- 使用 Pydantic 模型进行数据验证
- 确保接收到的消息格式正确

#### 3.3 聊天接口实现
```python
@app.post("/api/chat")
async def chat(message: Message):
    try:
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
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5
        }
```
- 使用 Qwen/QwQ-32B 模型
- 设置合适的参数控制输出质量
- 包含系统提示词，定义 AI 角色

#### 3.4 错误处理
```python
try:
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    raise HTTPException(status_code=500, detail=f"API请求错误: {str(e)}")
```
- 完善的错误处理机制
- 清晰的错误信息返回

### 4. 关键参数说明

#### 4.1 模型参数
- `max_tokens`: 512 - 限制响应长度
- `temperature`: 0.7 - 控制输出的随机性
- `top_p`: 0.7 - 控制输出的多样性
- `top_k`: 50 - 控制词汇选择范围
- `frequency_penalty`: 0.5 - 控制重复词汇的惩罚

#### 4.2 系统提示词
```python
"你是一个专业的心理咨询师，请以温暖、专业的态度回应用户的问题。"
```
- 定义 AI 的角色和行为
- 确保回复的专业性和温度

### 5. 安全性考虑
1. 环境变量管理敏感信息
2. CORS 配置允许跨域请求
3. 请求验证和错误处理
4. API 密钥保护

### 6. 性能优化
1. 异步处理请求
2. 合理的超时设置
3. 错误重试机制
4. 响应缓存（可选）

### 7. 部署说明
1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
创建 .env 文件并设置 API_TOKEN

3. 启动服务：
```bash
python main.py
```

### 8. 后续优化方向
1. 添加用户认证
2. 实现对话历史记录
3. 添加响应缓存
4. 实现流式响应
5. 添加日志记录
6. 实现健康检查接口
7. 添加监控指标
8. 优化错误处理机制 