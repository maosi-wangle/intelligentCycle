from datetime import datetime

from pydantic import BaseModel, Field


class AnswerCreateRequest(BaseModel):
    content: str = Field(min_length=1, examples=["可以使用 OAuth2PasswordBearer 和 JWT 工具库实现。"])


class AnswerPublic(BaseModel):
    id: int
    question_id: int
    content: str
    author: str
    like_count: int = 0
    is_accepted: bool = False
    created_at: datetime

