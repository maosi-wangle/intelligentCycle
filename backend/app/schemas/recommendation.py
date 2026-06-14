from datetime import datetime

from pydantic import BaseModel


class RecommendationItem(BaseModel):
    id: int
    title: str
    author: str
    tags: list[str]
    answer_count: int
    view_count: int
    like_count: int
    score: int
    created_at: datetime
