from typing import Optional

from pydantic.main import BaseModel

from app.db.serializer import InDBBaseSerializer


class UserCreateSerializer(BaseModel):
    name: str
    email: str
    hashed_password: Optional[str]


class UserUpdateSerializer(UserCreateSerializer):
    pass


class UserSerializer(InDBBaseSerializer):
    name: str
    email: str


class UserRegistrationSerializer(BaseModel):
    name: str
    email: str
    password: Optional[str] = None
