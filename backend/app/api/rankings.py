from fastapi import APIRouter

from app.api.questions import to_question_item
from app.schemas.common import ApiResponse
from app.schemas.question import QuestionListItem
from app.schemas.user import UserPublic
from app.services import mock_store


router = APIRouter(prefix="/rankings", tags=["rankings"])


@router.get("/hot-questions", response_model=ApiResponse[list[QuestionListItem]])
def hot_questions() -> ApiResponse[list[QuestionListItem]]:
    items = sorted(
        mock_store.questions,
        key=lambda item: item["view_count"] + item["answer_count"] * 5 + item["like_count"] * 3,
        reverse=True,
    )
    return ApiResponse(data=[to_question_item(item) for item in items])


@router.get("/users", response_model=ApiResponse[list[UserPublic]])
def user_rankings() -> ApiResponse[list[UserPublic]]:
    items = sorted(mock_store.users, key=lambda item: item["points"], reverse=True)
    return ApiResponse(data=[UserPublic(**item) for item in items])

