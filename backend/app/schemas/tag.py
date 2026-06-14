from pydantic import BaseModel, Field


class TagCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=32, examples=["FastAPI"])
    description: str = Field(default="", max_length=200, examples=["Python Web 后端框架"])


class TagPublic(BaseModel):
    id: int
    name: str
    description: str = ""

