# 智答圈接口文档

## 1. 接口规范

后端统一使用 FastAPI 提供 RESTful API。

本地开发地址：

```text
http://127.0.0.1:8000
```

Swagger 接口调试页面：

```text
http://127.0.0.1:8000/docs
```

基础路径：

```text
/api
```

统一响应格式：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

常见状态码：

| 状态码 | 含义 |
|---|---|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未登录或 Token 无效 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

需要登录的接口通过请求头传递 Token：

```text
Authorization: Bearer <token>
```

## 2. 用户认证接口

### 2.1 用户注册

```text
POST /api/auth/register
```

请求体：

```json
{
  "username": "student01",
  "password": "123456",
  "email": "student01@example.com"
}
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "username": "student01"
  }
}
```

### 2.2 用户登录

```text
POST /api/auth/login
```

请求体：

```json
{
  "username": "student01",
  "password": "123456"
}
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "access_token": "jwt-token",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "username": "student01"
    }
  }
}
```

### 2.3 获取当前用户信息

```text
GET /api/users/me
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "username": "student01",
    "email": "student01@example.com",
    "points": 120,
    "level": 3
  }
}
```

## 3. 问题接口

### 3.1 获取问题列表

```text
GET /api/questions
```

查询参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keyword | string | 否 | 搜索关键词 |
| tag_id | int | 否 | 标签 ID |
| page | int | 否 | 页码 |
| page_size | int | 否 | 每页数量 |

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 1,
    "items": [
      {
        "id": 1,
        "title": "FastAPI 如何实现 JWT 登录？",
        "content": "想了解 FastAPI 中 JWT 的基本实现方式。",
        "author": "student01",
        "tags": ["FastAPI", "JWT"],
        "answer_count": 2,
        "view_count": 30,
        "like_count": 5,
        "created_at": "2026-06-14T12:00:00"
      }
    ]
  }
}
```

### 3.2 发布问题

```text
POST /api/questions
```

请求体：

```json
{
  "title": "FastAPI 如何实现 JWT 登录？",
  "content": "想了解 FastAPI 中 JWT 的基本实现方式。",
  "tag_ids": [1, 2]
}
```

### 3.3 获取问题详情

```text
GET /api/questions/{question_id}
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "title": "FastAPI 如何实现 JWT 登录？",
    "content": "想了解 FastAPI 中 JWT 的基本实现方式。",
    "author": "student01",
    "tags": ["FastAPI", "JWT"],
    "view_count": 31,
    "like_count": 5,
    "is_collected": false,
    "created_at": "2026-06-14T12:00:00"
  }
}
```

## 4. 回答接口

### 4.1 获取问题回答列表

```text
GET /api/questions/{question_id}/answers
```

### 4.2 发布回答

```text
POST /api/questions/{question_id}/answers
```

请求体：

```json
{
  "content": "可以使用 OAuth2PasswordBearer 和 JWT 工具库实现。"
}
```

### 4.3 采纳最佳答案

```text
POST /api/answers/{answer_id}/accept
```

说明：仅问题发布者可以采纳回答。

## 5. 标签接口

### 5.1 获取标签列表

```text
GET /api/tags
```

### 5.2 创建标签

```text
POST /api/tags
```

请求体：

```json
{
  "name": "FastAPI",
  "description": "Python Web 后端框架"
}
```

## 6. 互动接口

### 6.1 点赞问题

```text
POST /api/questions/{question_id}/like
```

### 6.2 收藏问题

```text
POST /api/questions/{question_id}/collect
```

### 6.3 点赞回答

```text
POST /api/answers/{answer_id}/like
```

### 6.4 取消操作

```text
DELETE /api/questions/{question_id}/like
DELETE /api/questions/{question_id}/collect
DELETE /api/answers/{answer_id}/like
```

## 7. 排行榜接口

### 7.1 热榜问题

```text
GET /api/rankings/hot-questions
```

说明：根据浏览量、回答数、点赞数、收藏数和发布时间综合计算。

### 7.2 用户积分榜

```text
GET /api/rankings/users
```

说明：根据用户积分、回答数、采纳数和获赞数排序。

## 8. 推荐接口

### 8.1 推荐问题

```text
GET /api/recommendations/questions
```

说明：登录用户优先根据浏览历史、关注标签和热门问题推荐；未登录用户返回热榜内容。

## 9. AI Agent 接口

### 9.1 AI 智能问答

```text
POST /api/ai/ask
```

请求体：

```json
{
  "question": "FastAPI 登录接口应该怎么设计？",
  "use_retrieval": true
}
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "answer": "可以将登录接口设计为 POST /api/auth/login，登录成功后返回 JWT Token。",
    "sources": [
      {
        "type": "question",
        "id": 1,
        "title": "FastAPI 如何实现 JWT 登录？"
      }
    ]
  }
}
```

### 9.2 生成回答草稿

```text
POST /api/ai/draft-answer
```

请求体：

```json
{
  "question_id": 1
}
```

说明：AI Agent 根据问题内容、已有回答和检索结果生成回答草稿，不自动发布。

### 9.3 检索社区内容

```text
GET /api/ai/search
```

查询参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keyword | string | 是 | 检索关键词 |

说明：用于测试 Agent 的检索效果，可返回相关问题、回答和标签。
