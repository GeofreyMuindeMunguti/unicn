import enum

from app.partners.constants import PartnerMemberRoles


class MenuOptions(str, enum.Enum):
    DASHBOARD = "DASHBOARD"
    PARTNERS = "PARTNERS"
    KPI = "KPI"
    DEPARTMENTS = "DEPARTMENTS"
    PROFILE = "PROFILE"


MENU_ITEMS = {
    PartnerMemberRoles.SUPER_ADMIN.value: [
        MenuOptions.PARTNERS.value,
        MenuOptions.PROFILE.value,
        MenuOptions.DEPARTMENTS.value,
    ],
    PartnerMemberRoles.PARTNER_ADMIN.value: [
        MenuOptions.DASHBOARD.value,
        MenuOptions.DEPARTMENTS.value,
        MenuOptions.PROFILE.value,
        MenuOptions.KPI.value,
    ],
    PartnerMemberRoles.PARTNER_MEMBER.value: [
        MenuOptions.DASHBOARD.value,
        MenuOptions.KPI.value,
        MenuOptions.PROFILE.value,
    ],
    PartnerMemberRoles.CONSULTANT.value: [
        MenuOptions.DASHBOARD.value,
        MenuOptions.DEPARTMENTS.value,
        MenuOptions.KPI.value,
        MenuOptions.PROFILE.value,
    ]
}
