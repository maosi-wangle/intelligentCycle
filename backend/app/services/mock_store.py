from datetime import datetime, timezone


now = datetime.now(timezone.utc)

users = [
    {
        "id": 1,
        "username": "student01",
        "password": "123456",
        "email": "student01@example.com",
        "points": 120,
        "level": 3,
    }
]

tags = [
    {"id": 1, "name": "FastAPI", "description": "Python Web 后端框架"},
    {"id": 2, "name": "JWT", "description": "用户认证 Token"},
    {"id": 3, "name": "Vue", "description": "前端渐进式框架"},
]

questions = [
    {
        "id": 1,
        "title": "FastAPI 如何实现 JWT 登录？",
        "content": "想了解 FastAPI 中 JWT 的基本实现方式。",
        "author": "student01",
        "tag_ids": [1, 2],
        "answer_count": 1,
        "view_count": 30,
        "like_count": 5,
        "created_at": now,
        "is_collected": False,
    }
]

answers = [
    {
        "id": 1,
        "question_id": 1,
        "content": "可以使用 OAuth2PasswordBearer 和 JWT 工具库实现登录鉴权。",
        "author": "student01",
        "like_count": 3,
        "is_accepted": False,
        "created_at": now,
    }
]


def tag_names(tag_ids: list[int]) -> list[str]:
    tag_map = {tag["id"]: tag["name"] for tag in tags}
    return [tag_map[tag_id] for tag_id in tag_ids if tag_id in tag_map]


def next_id(items: list[dict]) -> int:
    return max((item["id"] for item in items), default=0) + 1

