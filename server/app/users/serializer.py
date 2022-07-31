from typing import Optional, Any, List

from pydantic.main import BaseModel
from pydantic.networks import EmailStr

from app.db.serializer import InDBBaseSerializer
from app.partners.serializer import PartnerMembershipSerializer


class UserCreateSerializer(BaseModel):
    name: Optional[str]
    email: str
    phone: Optional[str]
    hashed_password: Optional[str]


class UserUpdateSerializer(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    hashed_password: Optional[str]


class UserRegisterSerializer(BaseModel):
    password: Optional[str]
    name: Optional[str]
    user_id: Optional[str]


class UserMembershipsSerializer(InDBBaseSerializer):
    partner_name: str


class UserSerializer(InDBBaseSerializer):
    name: Optional[str]
    phone: Optional[str]
    email: str
    department_name: str = "Main - Office"
    memberships: Optional[List[PartnerMembershipSerializer]]


class UserRegistrationSerializer(BaseModel):
    name: Optional[str]
    email: str
    user_id: Optional[str]
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


class UserProfileUpdateSerializer(BaseModel):
    name: Optional[str]
    phone: Optional[str]
