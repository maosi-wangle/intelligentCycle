from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.recommendation import RecommendationItem
from app.services.recommendation_service import recommend_questions


router = APIRouter(prefix='/recommendations', tags=['recommendations'])


@router.get('/questions', response_model=ApiResponse[list[RecommendationItem]])
def get_recommendations(db: Session = Depends(get_db)) -> ApiResponse[list[RecommendationItem]]:
    return ApiResponse(data=recommend_questions(db))
