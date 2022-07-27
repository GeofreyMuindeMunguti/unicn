from http import HTTPStatus
from typing import Generator, Optional, Sequence

from pydantic.error_wrappers import ValidationError

from app.auth.dao import token_dao
from app.core.config import get_app_settings
from app.db.dao import LoadOption
from app.db.session import get_session, get_engine
from sqlalchemy.engine import Engine
from fastapi import Depends, Request

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from sqlalchemy.orm import Session, load_only

from app.exceptions.custom import HttpErrorException
from app.users.dao import user_dao
from app.users.models import User

settings = get_app_settings()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/access-token"
)


def get_db(engine: Engine = Depends(get_engine)) -> Generator:
    with get_session(engine=engine) as db:
        yield db


def get_current_active_user_id() -> str:
    return "ROOT"


def get_decoded_token(
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> dict:
    if not token:
        print("No token provided")
        raise HttpErrorException(
            status_code=HTTPStatus.UNAUTHORIZED,
            error_code="INACCURATE CREDENTIALS",
            error_message="INACCURATE CREDENTIALS",
        )
    try:
        # Temporary disable token expiry check on production environment.
        # TODO: Use redis for this.
        if request.url.path.endswith("validate/") or request.url.path.endswith(
            "refresh-token/"
        ):
            if not token_dao.is_refresh_token_valid(db, token=token):
                raise ValueError("Token not found.")
        else:
            if not token_dao.is_token_valid(db, token=token):
                # Token is expired, so we should return HTTP status 401.
                raise HttpErrorException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    error_code="ACCESS DENIED",
                    error_message="ACCESS DENIED",
                )
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": False},
        )
        return payload
    except (jwt.JWTError, ValidationError, ValueError) as e:
        print(f"Invalid token: {e}")
        raise HttpErrorException(
            status_code=HTTPStatus.FORBIDDEN,
            error_code="ACCESS_DENIED",
            error_message="ACCESS_DENIED",
        )


class CurrentUser:
    def __init__(self, load_options: Optional[Sequence[LoadOption]] = None) -> None:
        self.load_options = load_options

    def __call__(
        self,
        db: Session = Depends(get_db),
        token_payload: dict = Depends(get_decoded_token),
    ) -> User:
        load_options: Sequence[LoadOption] = [
            load_only(User.id, User.phone, User.email)
        ]
        if self.load_options:
            load_options = self.load_options
        user = user_dao.get(db, id=token_payload["user_id"], load_options=load_options)
        if not user:
            raise HttpErrorException(
                status_code=HTTPStatus.NOT_FOUND,
                error_code="USER NOT FOUND",
                error_message="User not found",
            )

        return user


def get_current_user(
    db: Session = Depends(get_db), token_payload: dict = Depends(get_decoded_token)
) -> User:
    user = user_dao.get(
        db,
        id=token_payload["user_id"],
    )
    if not user:
        raise HttpErrorException(
            status_code=HTTPStatus.NOT_FOUND,
            error_code="USER_CANNOT_BE_FOUND",
            error_message="USER_CANNOT_BE_FOUND",
        )

    return user
