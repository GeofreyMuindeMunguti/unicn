from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import deps
from app.users.models import User
from app.users.serializer import UserSerializer

router = APIRouter(prefix="/user")


@router.get("/me")
def user_profile(
    user: User = Depends(deps.get_current_user)
) -> UserSerializer:
    return user
