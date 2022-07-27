from app.db.dao import CRUDDao
from app.partners.models import Partner, PartnerMember
from app.partners.serializer import PartnerCreateSerializer, PartnerUpdateSerializer, PartnerMemberCreateSerializer, \
    PartnerMemberUpdateSerializer


class PartnerDao(
    CRUDDao[
        Partner,
        PartnerCreateSerializer,
        PartnerUpdateSerializer
    ]
):
    pass


partner_dao = PartnerDao(Partner)


class PartnerMemberDao(
    CRUDDao[
        PartnerMember,
        PartnerMemberCreateSerializer,
        PartnerMemberUpdateSerializer
    ]
):
    pass


partner_member_dao = PartnerMemberDao(PartnerMember)
