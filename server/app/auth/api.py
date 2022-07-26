
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dao import token_dao
from app.auth.serializer import LoginSerializer, LoginResponseSerializer
from app.core import deps
from app.exceptions.custom import HttpErrorException, DaoException

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
