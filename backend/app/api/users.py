from fastapi import APIRouter

from app.schemas.common import ApiResponse
from app.schemas.user import UserPublic
from app.services import mock_store


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=ApiResponse[UserPublic])
def get_current_user() -> ApiResponse[UserPublic]:
    return ApiResponse(data=UserPublic(**mock_store.users[0]))

