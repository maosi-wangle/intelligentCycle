from pydantic import BaseModel, Field


class AiAskRequest(BaseModel):
    question: str = Field(min_length=1, examples=['How should a FastAPI login API be designed?'])
    use_retrieval: bool = True
    conversation_id: str | None = Field(default=None, examples=['student-chat-001'])


class AiDraftAnswerRequest(BaseModel):
    question_id: int = Field(examples=[1])
    conversation_id: str | None = Field(default=None, examples=['student-chat-001'])


class AiSource(BaseModel):
    type: str
    id: int
    title: str
    snippet: str | None = None


class AiAnswerData(BaseModel):
    answer: str
    sources: list[AiSource] = []
    conversation_id: str | None = None
