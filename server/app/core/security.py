import datetime
from hashlib import md5
from typing import Any, Dict, Union

from jose import jwt
from passlib.context import CryptContext
from pydantic.main import BaseModel
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.session import Session

from app.core.config import get_app_settings
from app.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


class AccessTokenEncodePayload(BaseModel):
    expires_in: int
    user_id: str
    permissions: str
    grant_type: str


def create_access_token(
    db: Session, subject: Union[str, Any], grant_type: str, expires_in: int = None
) -> dict:
    settings = get_app_settings()
    expires_in_seconds = (
        expires_in if expires_in else settings.ACCESS_TOKEN_EXPIRY_IN_SECONDS
    )
    refresh_expires_in_seconds = settings.REFRESH_TOKEN_EXPIRY_IN_SECONDS
    to_encode = {
        # We need to use microseconds since multiple
        # tokens can be issued to the same user
        # in a second
        "iat": int(datetime.datetime.utcnow().timestamp() * 1000),
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(seconds=expires_in_seconds),
        "user_id": str(subject),
        "grant_type": grant_type,
    }
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    to_encode["exp"] = datetime.datetime.utcnow() + datetime.timedelta(
        seconds=refresh_expires_in_seconds
    )
    refresh_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    token_data = {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": grant_type,
        "expires_in": expires_in_seconds,
        "user_id": subject,
    }
    return token_data


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_request_hash(request_str: str) -> str:
    """
    Get a hash of a stringfied request.
    Using MD5 instead of something like sha256 since we want a cheap hash
    """
    return md5(bytes(request_str, "utf-8")).hexdigest()
