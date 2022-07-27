from typing import Optional, Any, List

from pydantic.main import BaseModel
from pydantic.networks import EmailStr

from app.db.serializer import InDBBaseSerializer
from app.partners.serializer import PartnerMembershipSerializer


class UserCreateSerializer(BaseModel):
    name: Optional[str]
    email: str
    hashed_password: Optional[str]


class UserUpdateSerializer(BaseModel):
    name: Optional[str]
    email: Optional[str]
    hashed_password: Optional[str]


class UserSerializer(InDBBaseSerializer):
    name: Optional[str]
    email: str


class UserRegistrationSerializer(BaseModel):
    name: str
    email: str
    password: Optional[str] = None


class UserLoginSerializer(InDBBaseSerializer):
    name: Optional[str]
    email: str
    memberships: Optional[List[PartnerMembershipSerializer]]


class UserInviteSerializer(BaseModel):
    email: EmailStr
    partner_id: str
    department_id: Optional[str]


class InvitedUserSerializer(InDBBaseSerializer):
    email: str
