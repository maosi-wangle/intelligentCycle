from fastapi import APIRouter

from app.api.questions import to_question_item
from app.schemas.common import ApiResponse
from app.schemas.question import QuestionListItem
from app.services import mock_store


router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/questions", response_model=ApiResponse[list[QuestionListItem]])
def recommend_questions() -> ApiResponse[list[QuestionListItem]]:
    items = sorted(
        mock_store.questions,
        key=lambda item: (item["like_count"], item["view_count"], item["created_at"]),
        reverse=True,
    )
    return ApiResponse(data=[to_question_item(item) for item in items])

