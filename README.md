# Intelligent Circle 智答圈

智答圈是一个面向学生与技术爱好者的知识分享与智能问答社区项目，用于《软件开发综合实践》课程开发。
项目以传统问答社区为基础，结合排行推荐与 AI 辅助问答能力，支持用户提问、回答、标签管理、问题检索、热榜查看与 AI 回答草稿生成。

## 项目内容

当前项目主要包含三部分：

- 社区核心：注册、登录、提问、回答、采纳答案、标签
- 社区增长：热门问题榜、用户排行榜、问题推荐
- AI 助手：基于 DeepSeek Flash 的 Agent 检索增强问答

## 技术栈

### 前端

- Vue 3
- Vite
- Vue Router
- Pinia

### 后端

- FastAPI
- SQLAlchemy
- SQLite（本地开发）
- JWT 鉴权
- OpenAPI / Swagger

### AI

- DeepSeek `deepseek-v4-flash`
- 基于问题、回答、标签的工具检索
- 轻量多轮对话记忆窗口

## 当前已完成功能

### 后端主体功能

- 用户注册与登录
- JWT 当前用户鉴权
- 问题列表、问题详情、发布问题
- 回答列表、发布回答、采纳回答
- 标签列表与新建标签
- 热门问题榜
- 用户排行榜
- 基础问题推荐

### AI 能力

- AI 检索搜索接口
- 基于 DeepSeek 的 AI 问答接口
- 基于题目内容的回答草稿生成
- 从 `backend/agent/persona.md` 加载助手人格
- 通过 `conversation_id` 支持轻量多轮上下文
- 未配置 API Key 时返回清晰错误信息

## 运行方式

在 `backend` 目录下执行：

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

启动后可访问：

- 服务地址：`http://127.0.0.1:8000`
- Swagger 文档：`http://127.0.0.1:8000/docs`

## 环境变量

请根据 `backend/.env.example` 创建本地 `backend/.env`。

```env
APP_NAME=Intelligent Circle API
APP_ENV=development
API_PREFIX=/api
DATABASE_URL=sqlite:///./app.db
JWT_SECRET_KEY=change-this-to-a-32-char-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
DEEPSEEK_API_KEY=your_deepseek_key
DEEPSEEK_MODEL=deepseek-v4-flash
```

## 目录结构

```text
backend/
  app/
    api/
    core/
    models/
    schemas/
    services/
  agent/
    persona.md
  .env.example
  requirements.txt

docs/
  api-design.md
```

## 说明

- `backend/.env.example` 请自行改为.env并配置api key
- 当前多轮记忆为进程内存，重启后端后会清空
- 当前数据库为 SQLite
