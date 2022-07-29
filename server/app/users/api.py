from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import deps
from app.exceptions.custom import HttpErrorException
from app.partners.dao import partner_member_dao
from app.users.dao import user_dao
from app.users.models import User
from app.users.serializer import UserSerializer, UserInviteSerializer, InvitedUserSerializer, UserUpdateSerializer, \
    UserRegisterSerializer

router = APIRouter(prefix="/user")


@router.get("/me/", response_model=UserSerializer)
def user_profile(
    user: User = Depends(deps.get_current_user)
) -> UserSerializer:
    return user


@router.post("/invite/", response_model=InvitedUserSerializer)
def invite_user(
    db: Session = Depends(deps.get_db),
    _: User = Depends(deps.get_current_user),
    *,
    obj_in: UserInviteSerializer,
) -> InvitedUserSerializer:
    user = user_dao.get_not_none(db, email=obj_in.email)
    if user and partner_member_dao.get_not_none(db, partner_id=obj_in.partner_id, user_id=user.id):
        raise HttpErrorException(
            status_code=HTTPStatus.BAD_REQUEST,
            error_code="USER INVITE FAILED",
            error_message="User exists!"
        )
    return user_dao.invite_user(db, obj_in=obj_in)
