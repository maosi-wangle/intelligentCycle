from pydantic import BaseModel, Field


class AiAskRequest(BaseModel):
    question: str = Field(min_length=1, examples=["FastAPI 登录接口应该怎么设计？"])
    use_retrieval: bool = True


class AiDraftAnswerRequest(BaseModel):
    question_id: int = Field(examples=[1])


class AiSource(BaseModel):
    type: str
    id: int
    title: str


class AiAnswerData(BaseModel):
    answer: str
    sources: list[AiSource] = []

