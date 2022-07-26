from typing import Optional

from app.core.security import get_password_hash, verify_password
from app.db.dao import CRUDDao
from app.users.models import User
from sqlalchemy.orm import Session
from app.users.serializer import UserCreateSerializer, UserUpdateSerializer, UserRegistrationSerializer


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


user_dao = UserDao(User)
