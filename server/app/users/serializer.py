from pydantic.main import BaseModel


class UserCreateSerializer(BaseModel):
    name: str


class UserUpdateSerializer(UserCreateSerializer):
    pass
