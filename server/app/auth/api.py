
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dao import token_dao
from app.auth.serializer import LoginSerializer, LoginResponseSerializer, PasswordResetSerializer, \
    PasswordResetResponseSerializer, GetPasswordResetCodeSerializer, ResetCodeSerializer
from app.core import deps
from app.exceptions.custom import HttpErrorException, DaoException
from app.users.dao import user_dao

router = APIRouter()


@router.post("/login")
def login(
    db: Session = Depends(deps.get_db),
    *,
    obj_in: LoginSerializer,
) -> LoginResponseSerializer:
    try:
        return token_dao.login(db, obj_in=obj_in)
    except DaoException:
        raise HttpErrorException(
            status_code=403,
            error_code="INVALID CREDENTIALS",
            error_message="Invalid credentials"
        )


@router.post("/password_reset")
def reset_password(
    db: Session = Depends(deps.get_db),
    *,
    obj_in: PasswordResetSerializer,
) -> PasswordResetResponseSerializer:
    try:
        return user_dao.password_reset(db, obj_in=obj_in)
    except DaoException as e:
        raise HttpErrorException(
            status_code=403,
            error_code="PASSWORD RESET FAILED",
            error_message=e.message,
        )


@router.post("/reset_code")
def get_reset_code(
    db: Session = Depends(deps.get_db),
    *,
    obj_in: GetPasswordResetCodeSerializer
) -> ResetCodeSerializer:
    try:
        return user_dao.get_password_reset_code(db, obj_in=obj_in)
    except DaoException as e:
        raise HttpErrorException(
            status_code=403,
            error_code="GET RESET CODE FAILED",
            error_message=e.message,
        )
