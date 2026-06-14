from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import LoginData, UserLoginRequest, UserPublic, UserRegisterRequest


def to_user_public(user: User) -> UserPublic:
    return UserPublic(
        id=user.id,
        username=user.username,
        email=user.email,
        points=user.points,
        level=user.level,
    )


def register_user(db: Session, payload: UserRegisterRequest) -> UserPublic:
    existing = db.scalar(select(User).where((User.username == payload.username) | (User.email == payload.email)))
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username or email already exists')

    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return to_user_public(user)


def login_user(db: Session, payload: UserLoginRequest) -> LoginData:
    user = db.scalar(select(User).where(User.username == payload.username))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

    return LoginData(
        access_token=create_access_token(str(user.id)),
        user=to_user_public(user),
    )
