from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.question import QuestionCreateRequest, QuestionDetail, QuestionListData
from app.services.question_service import collect_question, create_question, get_question_detail, like_question, list_questions


router = APIRouter(prefix='/questions', tags=['questions'])


@router.get('', response_model=ApiResponse[QuestionListData])
def get_questions(
    keyword: str | None = None,
    tag_id: int | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> ApiResponse[QuestionListData]:
    return ApiResponse(data=list_questions(db, keyword, tag_id, page, page_size))


@router.post('', response_model=ApiResponse[QuestionDetail], status_code=201)
def post_question(
    payload: QuestionCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[QuestionDetail]:
    return ApiResponse(data=create_question(db, current_user, payload))


@router.get('/{question_id}', response_model=ApiResponse[QuestionDetail])
def get_question(question_id: int, db: Session = Depends(get_db)) -> ApiResponse[QuestionDetail]:
    return ApiResponse(data=get_question_detail(db, question_id))


@router.post('/{question_id}/like', response_model=ApiResponse[dict])
def like(question_id: int, db: Session = Depends(get_db)) -> ApiResponse[dict]:
    return ApiResponse(data=like_question(db, question_id, True))


@router.delete('/{question_id}/like', response_model=ApiResponse[dict])
def unlike(question_id: int, db: Session = Depends(get_db)) -> ApiResponse[dict]:
    return ApiResponse(data=like_question(db, question_id, False))


@router.post('/{question_id}/collect', response_model=ApiResponse[dict])
def collect(question_id: int, db: Session = Depends(get_db)) -> ApiResponse[dict]:
    return ApiResponse(data=collect_question(db, question_id, True))


@router.delete('/{question_id}/collect', response_model=ApiResponse[dict])
def uncollect(question_id: int, db: Session = Depends(get_db)) -> ApiResponse[dict]:
    return ApiResponse(data=collect_question(db, question_id, False))
