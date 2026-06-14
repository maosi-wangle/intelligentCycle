from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.ai import AiAnswerData, AiAskRequest, AiDraftAnswerRequest
from app.schemas.common import ApiResponse
from app.services.agent_service import ask_with_agent, draft_answer_for_question
from app.services.retrieval_service import search_answers, search_questions, search_tags
from app.services.memory_service import conversation_memory


router = APIRouter(prefix='/ai', tags=['ai'])


@router.post('/ask', response_model=ApiResponse[AiAnswerData])
def ask_ai(payload: AiAskRequest, db: Session = Depends(get_db)) -> ApiResponse[AiAnswerData]:
    conversation_id = payload.conversation_id or conversation_memory.new_conversation_id()
    return ApiResponse(data=ask_with_agent(db, payload.question, payload.use_retrieval, conversation_id))


@router.post('/draft-answer', response_model=ApiResponse[AiAnswerData])
def draft_answer(payload: AiDraftAnswerRequest, db: Session = Depends(get_db)) -> ApiResponse[AiAnswerData]:
    conversation_id = payload.conversation_id or conversation_memory.new_conversation_id()
    return ApiResponse(data=draft_answer_for_question(db, payload.question_id, conversation_id))


@router.get('/search', response_model=ApiResponse[list[dict]])
def search_ai_context(keyword: str = Query(..., min_length=1), db: Session = Depends(get_db)) -> ApiResponse[list[dict]]:
    sources = [
        *search_questions(db, keyword, limit=5),
        *search_answers(db, keyword, limit=5),
        *search_tags(db, keyword, limit=5),
    ]
    return ApiResponse(data=[source.model_dump() for source in sources])
