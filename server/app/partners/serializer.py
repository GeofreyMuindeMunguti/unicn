from typing import Optional

from pydantic.main import BaseModel

from app.db.serializer import InDBBaseSerializer


class PartnerSerializer(BaseModel):
    name: str


class PartnerMembershipSerializer(InDBBaseSerializer):
    partner_id: str


class PartnerCreateSerializer(BaseModel):
    name: str
    address: str
    website_url: str
    logo_url: str


class PartnerUpdateSerializer(BaseModel):
    name: Optional[str]
    address: Optional[str]
    website_url: Optional[str]
    logo_url: Optional[str]


class PartnerSerializer(InDBBaseSerializer):
    name: str
    address: str
    website_url: str
    logo_url: str


class PartnerMemberCreateSerializer(BaseModel):
    partner_id: str
    user_id: str
    role: Optional[str] = None


class PartnerMemberUpdateSerializer(BaseModel):
    partner_id: str
    user_id: str
    role: Optional[str] = None
