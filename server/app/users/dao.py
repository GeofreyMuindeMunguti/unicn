from app.db.dao import CRUDDao
from app.users.models import User
from app.users.serializer import UserCreateSerializer, UserUpdateSerializer


class UserDao(CRUDDao[User, UserCreateSerializer, UserUpdateSerializer]):
    pass


user_dao = UserDao(User)
