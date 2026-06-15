from datetime import datetime

from pydantic import BaseModel, Field


class QuestionCreateRequest(BaseModel):
    title: str = Field(min_length=4, max_length=120, examples=["FastAPI 如何实现 JWT 登录？"])
    content: str = Field(min_length=1, examples=["想了解 FastAPI 中 JWT 的基本实现方式。"])
    tag_ids: list[int] = Field(default_factory=list, examples=[[1, 2]])


class QuestionListItem(BaseModel):
    id: int
    title: str
    content: str
    author: str
    tags: list[str]
    answer_count: int
    view_count: int
    like_count: int
    created_at: datetime


class QuestionDetail(QuestionListItem):
    is_collected: bool = False
    collect_count: int = 0


class QuestionListData(BaseModel):
    total: int
    items: list[QuestionListItem]