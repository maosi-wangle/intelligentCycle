from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.user import UserPublic
from app.services.auth_service import to_user_public


router = APIRouter(prefix='/users', tags=['users'])


@router.get('/me', response_model=ApiResponse[UserPublic])
def get_current_user_profile(current_user: User = Depends(get_current_user)) -> ApiResponse[UserPublic]:
    return ApiResponse(data=to_user_public(current_user))
