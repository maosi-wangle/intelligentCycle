from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.ranking import HotQuestionItem, UserRankingItem
from app.services.ranking_service import list_hot_questions, list_user_rankings


router = APIRouter(prefix='/rankings', tags=['rankings'])


@router.get('/hot-questions', response_model=ApiResponse[list[HotQuestionItem]])
def get_hot_questions(db: Session = Depends(get_db)) -> ApiResponse[list[HotQuestionItem]]:
    return ApiResponse(data=list_hot_questions(db))


@router.get('/users', response_model=ApiResponse[list[UserRankingItem]])
def get_user_rankings(db: Session = Depends(get_db)) -> ApiResponse[list[UserRankingItem]]:
    return ApiResponse(data=list_user_rankings(db))
