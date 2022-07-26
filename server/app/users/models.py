from app.db.base_class import Base
from sqlalchemy import Column, String


class User(Base):
    __tablename__ = "users"

    name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=False)
    hashed_password = Column(String, nullable=True)
