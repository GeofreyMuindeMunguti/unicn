from typing import Optional, List

from pydantic.main import BaseModel

from app.db.serializer import InDBBaseSerializer


class PartnerSerializer(BaseModel):
    name: str


class PartnerMembershipSerializer(InDBBaseSerializer):
    partner_id: str
    partner_name: str
    menu_items: Optional[List[str]]


class PartnerOwnerSerializer(BaseModel):
    email: str
    phone: Optional[str]
    name: str


class PartnerCreateSerializer(BaseModel):
    name: str
    address: str
    website_url: str
    logo_url: str
    owner_id: Optional[str]
    owner: PartnerOwnerSerializer


class PartnerUpdateSerializer(BaseModel):
    name: Optional[str]
    address: Optional[str]
    website_url: Optional[str]
    logo_url: Optional[str]


class PartnerSerializer(InDBBaseSerializer):
    name: str
    address: Optional[str]
    website_url: Optional[str]
    logo_url: Optional[str]


class PartnerMemberCreateSerializer(BaseModel):
    partner_id: str
    user_id: str
    role: Optional[str] = None


class PartnerMemberUpdateSerializer(BaseModel):
    partner_id: str
    user_id: str
    role: Optional[str] = None
