import json
import os
from math import ceil
from typing import Generic, Optional, Sequence, TypeVar, cast

from fastapi_pagination import Params, create_page, resolve_params
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from fastapi_pagination.ext.sqlalchemy import paginate_query
from pydantic import BaseModel, Field, conint
from sqlalchemy import DDL, func, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select

from app.db.session import get_session

T = TypeVar("T")


path = os.path.dirname(os.path.abspath(__file__))


class PaginationQueryParams(BaseModel, AbstractParams):
    page: conint(ge=1) = Field(1, deprecated=True)  # type: ignore
    per_page: int = 100

    def to_raw_params(self) -> RawParams:
        return RawParams(limit=self.per_page, offset=(self.page - 1) * self.per_page)


class Page(AbstractPage[T], Generic[T]):
    items: Sequence[T]
    total: conint(ge=0)  # type: ignore
    current_page: int
    next_page: int
    total_pages: int

    __params_type__ = PaginationQueryParams

    @classmethod
    def create(
        cls, items: Sequence[T], total: int, params: AbstractParams
    ) -> "Page[T]":
        raw = params.to_raw_params()
        if raw.limit == 0:
            total_pages = 0
        else:
            total_pages = int(ceil(total / float(raw.limit)))

        current_page = int((raw.offset / raw.limit) + 1)

        if current_page >= total_pages:
            next_page = -1
        else:
            next_page = current_page + 1

        return cls(
            items=items,
            total=total,
            current_page=current_page,
            next_page=next_page,
            total_pages=total_pages,
        )


Pagination = TypeVar("Pagination", bound=AbstractPage)


def get_total_count(query: Select) -> int:
    # Inspired from
    # https://gist.github.com/noviluni/d86adfa24843c7b8ed10c183a9df2afe
    with get_session() as db:
        return db.scalar(select(func.count()).select_from(query.subquery()))


def paginate(
    db: Session,
    query: Select,
    total_query: Optional[Select] = None,
    params: Optional[AbstractParams] = None,
) -> AbstractPage:
    params = resolve_params(params)
    query = paginate_query(query, params)
    result = db.scalars(query)
    items = [item for item in result.unique().all()]
    total = get_total_count(query=total_query)
    return Page.create(items, total, params)
