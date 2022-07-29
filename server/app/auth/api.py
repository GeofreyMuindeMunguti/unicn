
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dao import token_dao
from app.auth.serializer import LoginSerializer, LoginResponseSerializer, PasswordResetSerializer, GetPasswordResetCodeSerializer, ResetCodeSerializer
from app.core import deps
from app.exceptions.custom import HttpErrorException, DaoException
from app.users.dao import user_dao
from app.users.serializer import UserSerializer, UserRegisterSerializer, UserRegistrationSerializer

router = APIRouter(prefix="/auth")


@router.post("/login/", response_model=LoginResponseSerializer)
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


@router.post("/password-reset/", response_model=UserSerializer)
def reset_password(
    db: Session = Depends(deps.get_db),
    *,
    obj_in: PasswordResetSerializer,
) -> UserSerializer:
    try:
        return user_dao.password_reset(db, obj_in=obj_in)
    except DaoException as e:
        raise HttpErrorException(
            status_code=403,
            error_code="PASSWORD RESET FAILED",
            error_message=e.message,
        )


@router.post("/reset-code/", response_model=ResetCodeSerializer)
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


@router.post("/register", response_model=UserSerializer)
def update_user_details(
    db: Session = Depends(deps.get_db),
    *,
    obj_in: UserRegistrationSerializer,
) -> UserSerializer:
    return user_dao.register(db, obj_in=obj_in)
