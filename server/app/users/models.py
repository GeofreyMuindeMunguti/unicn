from app.db.base_class import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.partners.models import PartnerMember


class User(Base):
    __tablename__ = "users"

    name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String, nullable=True)
    reset_code = Column(String, nullable=True)

    memberships: "PartnerMember" = relationship(
        "PartnerMember",
        back_populates="user"
    )
