from random import randint
from typing import Optional

from app.auth.serializer import PasswordResetSerializer, GetPasswordResetCodeSerializer
from app.core.config import get_app_settings
from app.core.security import get_password_hash, verify_password
from app.db.dao import CRUDDao, ChangedObjState
from app.exceptions.custom import DaoException
from app.partners.dao import partner_dao, partner_member_dao
from app.partners.serializer import PartnerMemberCreateSerializer
from app.users.models import User
from sqlalchemy.orm import Session, selectinload
from app.users.serializer import UserCreateSerializer, UserUpdateSerializer, UserRegistrationSerializer, \
    UserInviteSerializer
from app.utils.email import send_email


class UserDao(CRUDDao[User, UserCreateSerializer, UserUpdateSerializer]):
    def register(self, db: Session, obj_in: UserRegistrationSerializer) -> User:
        if obj_in.password:
            hashed_password = get_password_hash(obj_in.password)

            obj_in = UserCreateSerializer(hashed_password=hashed_password, **obj_in.dict(exclude_unset=True))

        else:
            obj_in = UserCreateSerializer(**obj_in.dict(exclude_unset=True))

        return self.create(db, obj_in=obj_in)

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = self.get(
            db, email=email
        )
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def password_reset(self, db: Session, obj_in: PasswordResetSerializer) -> User:
        user = self.get(
            db, email=obj_in.email
        )
        if not user:
            raise DaoException(resource="USER", message="User not found!")

        if user.reset_code != obj_in.reset_code:
            raise DaoException(resource="USER", message="User password reset failed!")

        hashed_password = get_password_hash(obj_in.password)
        obj_in = UserUpdateSerializer(hashed_password=hashed_password)

        return self.update(db, db_obj=user, obj_in=obj_in.dict(exclude_unset=True))

    def get_password_reset_code(self, db: Session, obj_in: GetPasswordResetCodeSerializer) -> User:
        user = self.get(
            db, email=obj_in.email
        )
        if not user:
            raise DaoException(
                resource="USER", message="User not found!"
            )

        reset_code = randint(1000, 9999)
        send_email(
            email_to=user.email,
            subject_template="Password reset",
            html_template=f"Here is your password reset code: {user.reset_code}"
        )
        user.reset_code = reset_code

        db.commit()
        db.refresh(user)

        return user

    def send_invitation(self, db: Session, user_id: str) -> None:
        user = self.get_not_none(db, id=user_id)
        settings = get_app_settings()

        try:
            send_email(
                email_to=user.email,
                subject_template="Invite Email",
                html_template=f"You have been invited to UNICON, click "
                              f"<a href='{settings.REGISTER_URL}?id={user_id}'>Here</a>"
            )
        except Exception:
            raise DaoException(
                resource="INVITE EMAIL",
                message="Could not send reset email!"
            )

    def on_post_update(
        self, db: Session, db_obj: User, changed: ChangedObjState
    ) -> None:
        if changed.get("hashed_password", None):
            db_obj.reset_code = None
            db.commit()

    def invite_user(self, db: Session, obj_in: UserInviteSerializer) -> User:
        partner = partner_dao.get_not_none(db, id=obj_in.partner_id)
        user_obj_in = UserCreateSerializer(
            email=obj_in.email
        )
        user = self.create(db, obj_in=user_obj_in)
        partner_member_dao.create(db, obj_in=PartnerMemberCreateSerializer(user_id=user.id, partner_id=partner.id))
        db.refresh(user)

        if user:
            settings = get_app_settings()
            send_email(
                email_to=obj_in.email,
                subject_template="INVITE EMAIL",
                html_template=f"You have been invited to {partner.name} to join click here <a href='{settings.REGISTER_URL}?user_id={user.id}&partner_name={partner.name}'></a>"
            )
        return user


user_dao = UserDao(User, load_options=[
    selectinload(User.memberships)
])
