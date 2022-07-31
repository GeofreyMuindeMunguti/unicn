import enum


class PartnerMemberRoles(str, enum.Enum):
    PARTNER_MEMBER = "PARTNER_MEMBER"
    PARTNER_ADMIN = "PARTNER_ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"
    CONSULTANT = "CONSULTANT"
