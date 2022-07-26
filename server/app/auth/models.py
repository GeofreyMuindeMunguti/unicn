from app.db.base_class import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Boolean, Index, UniqueConstraint


class AuthToken(Base):
    __tablename__ = "auth_token"

    access_token = Column(String, nullable=False, index=True, unique=True)
    refresh_token = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("users.id"))
    token_type: str = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    expires_at: datetime = Column(DateTime, nullable=False)
    expires_in = Column(Integer, nullable=False)

    user: "User" = relationship(
        "User",
        foreign_keys=[user_id],
    )

    __table_args__ = (
        UniqueConstraint("access_token", "user_id", "token_type", "is_active"),
    )

    @property
    def is_invalid(self) -> bool:
        return (not self.is_active) or (datetime.utcnow() > self.expires_at)


# We fetch an auth_token in descending by default filtered by
# the access token value
Index(
    "idx_auth_token_access_token_created_at",
    AuthToken.access_token,
    AuthToken.created_at.desc(),
)
