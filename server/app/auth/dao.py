from datetime import datetime, timedelta

from sqlalchemy.orm import Session, load_only, noload, selectinload, joinedload

from app.auth.models import AuthToken
from app.core.security import create_access_token
from app.auth.serializer import (
    TokenCreateSerializer,
    TokenGrantType,
    TokenInDBInDBBaseSerializer, LoginSerializer,
)

from app.db.dao import CRUDDao
from app.exceptions.custom import DaoException
from app.partners.models import PartnerMember
from app.users.models import User


class TokenDao(
    CRUDDao[AuthToken, TokenCreateSerializer, TokenInDBInDBBaseSerializer]
):
    def on_pre_create(
        self, db: Session, pk: str, values: dict, orig_values: dict
    ) -> None:
        token_data = create_access_token(
            db=db,
            subject=orig_values["user_id"],
            grant_type=orig_values["token_type"].value,
        )
        values["access_token"] = token_data["access_token"]
        values["refresh_token"] = token_data["refresh_token"]
        values["user_id"] = orig_values["user_id"]
        values["token_type"] = orig_values["token_type"].value
        values["expires_in"] = token_data["expires_in"]
        values["expires_at"] = datetime.utcnow() + timedelta(
            seconds=token_data["expires_in"]
        )
        values["is_active"] = True

    def get_user_active_token(self, db: Session, *, user_id: str) -> AuthToken:
        # Create and return a new token
        obj_in = TokenCreateSerializer(
            user_id=user_id, token_type=TokenGrantType.CLIENT_CREDENTIALS.value
        )
        return token_dao.create(db, obj_in=obj_in)

    def is_token_valid(self, db: Session, token: str) -> bool:
        token_obj = self.get(
            db, load_options=[load_only(AuthToken.expires_at)], access_token=token
        )
        token_eat = token_obj.expires_at if token_obj else None
        return token_eat is not None and token_eat >= datetime.utcnow()

    def is_refresh_token_valid(self, db: Session, token: str) -> bool:
        token_obj = self.get(
            db, load_options=[load_only(AuthToken.id)], refresh_token=token
        )
        token_id = token_obj.id if token_obj else None
        return token_id is not None

    def refresh_token(
        self, db: Session, token: str, is_refresh: bool = False
    ) -> AuthToken:
        auth_token = self.get_not_none(db, refresh_token=token)

        token_data = create_access_token(
            db=db,
            subject=auth_token.user_id,
            grant_type=auth_token.token_type,
        )
        if is_refresh:
            data = {"refresh_token": token_data["refresh_token"]}
        else:
            data = {
                "access_token": token_data["access_token"],
                "expires_in": token_data["expires_in"],
                "expires_at": datetime.utcnow()
                + timedelta(seconds=token_data["expires_in"]),
                "is_active": True,
            }
        return self.update(db, db_obj=auth_token, obj_in=data)

    def login(self, db: Session, obj_in: LoginSerializer) -> AuthToken:
        from app.users.dao import user_dao

        user = user_dao.authenticate(db, email=obj_in.email, password=obj_in.password)
        if not user:
            raise DaoException(
                resource="AUTH",
                message="Authentication failed, confirm credentials"
            )

        token = self.get(db, user_id=user.id)
        if not token:
            self.create(db, obj_in=TokenCreateSerializer(user_id=user.id, token_type=TokenGrantType.AUTHORIZATION_CODE))

        token = self.get(db, user_id=user.id, load_options=[
            joinedload(AuthToken.user).options(
                joinedload(User.memberships).options(joinedload(PartnerMember.partner))
            )
        ])
        return token


token_dao = TokenDao(AuthToken, load_options=[joinedload(AuthToken.user).options(
    joinedload(User.memberships).options(joinedload(PartnerMember.partner))
)])
