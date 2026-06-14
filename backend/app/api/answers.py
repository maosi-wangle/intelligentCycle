from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.answer import AnswerCreateRequest, AnswerPublic
from app.schemas.common import ApiResponse
from app.services.answer_service import accept_answer, create_answer, like_answer, list_answers


router = APIRouter(tags=['answers'])


@router.get('/questions/{question_id}/answers', response_model=ApiResponse[list[AnswerPublic]])
def get_answers(question_id: int, db: Session = Depends(get_db)) -> ApiResponse[list[AnswerPublic]]:
    return ApiResponse(data=list_answers(db, question_id))


@router.post('/questions/{question_id}/answers', response_model=ApiResponse[AnswerPublic], status_code=201)
def post_answer(
    question_id: int,
    payload: AnswerCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[AnswerPublic]:
    return ApiResponse(data=create_answer(db, question_id, current_user, payload))


@router.post('/answers/{answer_id}/accept', response_model=ApiResponse[AnswerPublic])
def accept(answer_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> ApiResponse[AnswerPublic]:
    return ApiResponse(data=accept_answer(db, answer_id, current_user))


@router.post('/answers/{answer_id}/like', response_model=ApiResponse[dict])
def like(answer_id: int, db: Session = Depends(get_db)) -> ApiResponse[dict]:
    return ApiResponse(data=like_answer(db, answer_id, True))


@router.delete('/answers/{answer_id}/like', response_model=ApiResponse[dict])
def unlike(answer_id: int, db: Session = Depends(get_db)) -> ApiResponse[dict]:
    return ApiResponse(data=like_answer(db, answer_id, False))
