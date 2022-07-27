from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.users.serializer import UserSerializer


class TokenGrantType(Enum):
    IMPLICIT = "implict"
    AUTHORIZATION_CODE = "authorization_code"
    CLIENT_CREDENTIALS = "client_credentials"
    PASSWORD = "password"
    REFRESH_TOKEN = "refresh_token"


class TokenBaseSerializer(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: TokenGrantType
    user_id: str


class TokenCreateSerializer(BaseModel):
    token_type: TokenGrantType
    user_id: str


class TokenReadSerializer(BaseModel):
    user: UserSerializer
    access_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str


class TokenInDBInDBBaseSerializer(TokenBaseSerializer):
    id: str
    expires_at: datetime
    expires_in: int
    is_active: bool
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class TokenSerializer(TokenInDBInDBBaseSerializer):
    pass


class LoginSerializer(BaseModel):
    email: str
    password: str


class LoginResponseSerializer(TokenInDBInDBBaseSerializer):
    user: UserSerializer


class PasswordResetResponseSerializer(UserSerializer):
    pass


class PasswordResetSerializer(BaseModel):
    email: str
    password: str
    reset_code: str


class GetPasswordResetCodeSerializer(BaseModel):
    email: str


class ResetCodeSerializer(BaseModel):
    reset_code: str
