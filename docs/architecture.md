# 智答圈系统架构设计

## 1. 总体架构

智答圈采用前后端分离架构。前端使用 Vue 3 构建用户界面，后端使用 FastAPI 提供 RESTful API，数据库保存用户、问题、回答、标签、互动和积分数据。

AI 扩展部分通过后端服务接入 DeepSeek Flash API，并结合社区已有数据实现工具检索型 Agentic RAG。该方案不使用 embedding 和向量数据库，而是通过关键词检索、标签匹配和可选 BM25 排序召回相关内容，再由大模型生成回答。

```text
用户浏览器
   |
   v
Vue 3 前端
   |
   v
FastAPI 后端
   |
   +--> 业务数据库
   |
   +--> 检索服务
   |
   +--> DeepSeek Flash API
```

## 2. 前端架构

前端主要负责页面展示、用户交互、状态管理和接口调用。

推荐目录结构：

```text
frontend/
  src/
    api/
      auth.ts
      question.ts
      answer.ts
      tag.ts
      ranking.ts
      ai.ts
    components/
    views/
      LoginView.vue
      RegisterView.vue
      HomeView.vue
      QuestionDetailView.vue
      ProfileView.vue
      RankingView.vue
      AiAssistantView.vue
    router/
    stores/
    utils/
```

前端核心页面：

| 页面 | 说明 |
|---|---|
| 登录注册页 | 用户登录、注册 |
| 首页 | 展示问题流、搜索框、热门标签 |
| 问题详情页 | 展示问题内容、回答列表、点赞收藏、AI 回答草稿入口 |
| 发布问题页 | 创建新问题并绑定标签 |
| 个人中心 | 用户资料、积分、发布记录、收藏记录 |
| 排行榜页 | 热榜问题和用户积分榜 |
| AI 助手页 | 与 AI Agent 对话，展示检索来源 |

## 3. 后端架构

后端使用 FastAPI，按路由层、服务层、数据模型层划分。

推荐目录结构：

```text
backend/
  app/
    main.py
    api/
      auth.py
      users.py
      questions.py
      answers.py
      tags.py
      interactions.py
      rankings.py
      recommendations.py
      ai.py
    services/
      auth_service.py
      question_service.py
      answer_service.py
      ranking_service.py
      recommend_service.py
      retrieval_service.py
      agent_service.py
      deepseek_service.py
    models/
      user.py
      question.py
      answer.py
      tag.py
      interaction.py
    schemas/
    core/
      config.py
      security.py
      database.py
```

后端分层说明：

| 层级 | 作用 |
|---|---|
| api | 定义接口路径、接收请求、返回响应 |
| services | 编写业务逻辑，如积分计算、热榜计算、AI 调用 |
| models | 定义数据库表结构 |
| schemas | 定义请求和响应数据格式 |
| core | 保存配置、数据库连接、安全认证等公共能力 |

## 4. 数据库设计概览

主要数据表：

| 表名 | 说明 |
|---|---|
| users | 用户信息、积分、等级 |
| questions | 问题标题、内容、作者、浏览量 |
| answers | 回答内容、作者、所属问题、是否被采纳 |
| tags | 标签名称和描述 |
| question_tags | 问题和标签的多对多关系 |
| likes | 点赞记录 |
| collections | 收藏记录 |
| view_logs | 浏览记录，用于推荐 |

核心关系：

```text
users 1 - n questions
users 1 - n answers
questions 1 - n answers
questions n - n tags
users n - n questions through collections
users n - n questions/answers through likes
```

## 5. AI Agentic RAG 架构

本项目采用轻量级工具检索型 Agentic RAG，不使用 embedding 和向量数据库。

整体流程：

```text
用户问题
   |
   v
AI Agent 判断是否需要检索
   |
   v
调用检索工具
   |
   +--> search_questions
   +--> search_answers
   +--> search_tags
   +--> get_question_detail
   +--> get_hot_questions
   |
   v
整理检索结果
   |
   v
调用 DeepSeek Flash 生成回答
   |
   v
返回答案和参考来源
```

Agent 可用工具：

| 工具 | 作用 |
|---|---|
| search_questions | 根据关键词检索问题标题和内容 |
| search_answers | 根据关键词检索历史回答 |
| search_tags | 根据标签名称检索相关问题 |
| get_question_detail | 获取指定问题及其回答 |
| get_hot_questions | 获取当前热榜问题 |

检索策略：

1. 从用户问题中提取关键词。
2. 优先匹配问题标题、问题内容和标签。
3. 对命中的内容按相关度、点赞数、采纳状态和浏览量排序。
4. 将排序靠前的结果作为上下文交给 DeepSeek Flash。
5. AI 生成答案时返回参考来源，便于用户判断可信度。

## 6. 核心业务流程

### 6.1 用户提问流程

```text
用户登录
  -> 发布问题
  -> 选择标签
  -> 后端保存问题
  -> 首页和标签页展示新问题
```

### 6.2 用户回答与采纳流程

```text
用户查看问题详情
  -> 发布回答
  -> 提问者查看回答
  -> 采纳最佳答案
  -> 系统给回答者增加积分
```

### 6.3 推荐流程

```text
用户访问首页
  -> 后端读取浏览记录和关注标签
  -> 结合热度分数排序
  -> 返回推荐问题列表
```

### 6.4 AI 辅助回答流程

```text
用户进入 AI 助手或问题详情页
  -> 输入问题或点击生成回答草稿
  -> Agent 检索相关社区内容
  -> DeepSeek Flash 生成回答
  -> 前端展示答案和来源
```

## 7. 设计原则

1. 主系统优先，AI 模块作为扩展能力。
2. 接口先行，前后端通过 API 文档协作。
3. 模块 Owner 制，每个成员负责明确的功能边界。
4. AI 生成内容不自动发布，由用户确认后再使用。
5. 检索结果需要展示来源，提升可解释性。

