import base64
import os
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, MetaData, String
from sqlalchemy.orm import Mapped, declarative_base
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.sqltypes import Boolean

from app.db.custom_search import make_searchable
from app.db.mixins import FilterSortMixin, InspectionMixin


def get_current_datetime() -> datetime:
    return datetime.now()


def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_unique_string(len: int = 6) -> str:
    """Generate a base"""
    return base64.b32encode(os.urandom(len)).decode("utf-8")[:len]


def generate_fake_email() -> str:
    return f"{uuid.uuid4()}@fake.rejareja.app"


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

meta = MetaData(naming_convention=convention)

BaseClass = declarative_base()


class Base(BaseClass, FilterSortMixin, InspectionMixin):
    __abstract__ = True

    id: Mapped[str] = Column(String, primary_key=True, default=generate_uuid)
    created_at: Mapped[datetime] = Column(
        DateTime, default=get_current_datetime, nullable=False
    )
    updated_at = Column(
        DateTime, default=None, onupdate=get_current_datetime, nullable=True
    )


make_searchable(Base.metadata)


class ActiveBaseAbstract(object):
    is_active: Mapped[bool] = Column(  # type: ignore [assignment]
        Boolean, server_default=true(), default=True
    )
