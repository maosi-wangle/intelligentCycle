from fastapi import APIRouter, HTTPException

from app.schemas.common import ApiResponse
from app.schemas.user import LoginData, UserLoginRequest, UserPublic, UserRegisterRequest
from app.services import mock_store


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=ApiResponse[UserPublic])
def register(payload: UserRegisterRequest) -> ApiResponse[UserPublic]:
    if any(user["username"] == payload.username for user in mock_store.users):
        raise HTTPException(status_code=400, detail="用户名已存在")

    user = {
        "id": mock_store.next_id(mock_store.users),
        "username": payload.username,
        "password": payload.password,
        "email": payload.email,
        "points": 0,
        "level": 1,
    }
    mock_store.users.append(user)
    return ApiResponse(data=UserPublic(**user))


@router.post("/login", response_model=ApiResponse[LoginData])
def login(payload: UserLoginRequest) -> ApiResponse[LoginData]:
    user = next(
        (
            item
            for item in mock_store.users
            if item["username"] == payload.username and item["password"] == payload.password
        ),
        None,
    )
    if user is None:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    return ApiResponse(
        data=LoginData(
            access_token=f"mock-token-{user['id']}",
            user=UserPublic(**user),
        )
    )

