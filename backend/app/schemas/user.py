from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    username: str = Field(min_length=2, max_length=32, examples=["student01"])
    password: str = Field(min_length=6, max_length=64, examples=["123456"])
    email: EmailStr = Field(examples=["student01@example.com"])


class UserLoginRequest(BaseModel):
    username: str = Field(examples=["student01"])
    password: str = Field(examples=["123456"])


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None
    points: int = 0
    level: int = 1


class LoginData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic

