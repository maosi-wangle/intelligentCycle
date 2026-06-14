from datetime import datetime

from pydantic import BaseModel


class HotQuestionItem(BaseModel):
    id: int
    title: str
    author: str
    tags: list[str]
    answer_count: int
    view_count: int
    like_count: int
    score: int
    created_at: datetime


class UserRankingItem(BaseModel):
    id: int
    username: str
    points: int
    level: int
    answer_count: int
    accepted_count: int
    like_count: int
    score: int
