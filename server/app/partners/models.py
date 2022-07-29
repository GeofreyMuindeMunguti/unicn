from app.db.base_class import Base, ActiveBaseAbstract
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.partners.constants import PartnerMemberRoles


class Partner(Base, ActiveBaseAbstract):
    __tablename__ = "partners"

    name = Column(String(200), nullable=False, unique=True)
    address = Column(String(100), nullable=True)
    website_url = Column(String(100), nullable=True, unique=True)
    logo_url = Column(String(100), nullable=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=True)

    members: "PartnerMember" = relationship(
        "PartnerMember",
        back_populates="partner"
    )
    owner: "User" = relationship(
        "User"
    )

    @property
    def member_count(self) -> int:
        return len(self.members)


class PartnerMember(Base, ActiveBaseAbstract):
    __tablename__ = "partnermembers"

    partner_id = Column(String, ForeignKey("partners.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False, default=PartnerMemberRoles.PARTNER_MEMBER.value)

    partner: "Partner" = relationship(
        "Partner",
        foreign_keys=[partner_id],
        back_populates="members"
    )
    user: "User" = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="memberships"
    )

    __table_args__ = (
        UniqueConstraint(
            "partner_id",
            "user_id",
            name="uq_partner_user"
        ),
    )
