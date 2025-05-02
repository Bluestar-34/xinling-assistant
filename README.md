# 心聆助手

一个基于 Vue 3 和 FastAPI 的网页对话应用，提供心理咨询服务。

## 项目结构

```
.
├── backend/             # 后端代码
│   └── main.py         # FastAPI 主程序
├── frontend/           # 前端代码
│   ├── src/           # Vue 源代码
│   └── index.html     # 主页面
├── requirements.txt    # Python 依赖
└── .env               # 环境变量（需要自行创建）
```

## 安装步骤

1. 安装后端依赖：
```bash
pip install -r requirements.txt
```

2. 创建 .env 文件并添加你的 OpenAI API 密钥：
```
OPENAI_API_KEY=your_api_key_here
```

3. 安装前端依赖：
```bash
cd frontend
npm install
```

## 运行项目

1. 启动后端服务：
```bash
cd backend
python main.py
```

2. 启动前端开发服务器：
```bash
cd frontend
npm run dev
```

3. 在浏览器中访问 http://localhost:5173

## 功能特点

- 简洁的对话界面
- 实时响应
- 专业的心理咨询服务
- 支持长对话
- 响应式设计

## 注意事项

- 请确保你有有效的 OpenAI API 密钥
- 在生产环境中部署时，请修改 CORS 设置
- 建议使用 Python 3.8+ 版本 