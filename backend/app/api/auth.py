from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.user import LoginData, UserPublic, UserLoginRequest, UserRegisterRequest
from app.services.auth_service import login_user, register_user


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=ApiResponse[UserPublic])
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)) -> ApiResponse[UserPublic]:
    return ApiResponse(data=register_user(db, payload))


@router.post('/login', response_model=ApiResponse[LoginData])
def login(payload: UserLoginRequest, db: Session = Depends(get_db)) -> ApiResponse[LoginData]:
    return ApiResponse(data=login_user(db, payload))
