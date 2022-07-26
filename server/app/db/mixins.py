import operator as operators
from typing import Any, Dict, Type

from sqlalchemy import asc, desc, inspect
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.sql import operators as sql_operators
from sqlalchemy_utils import get_columns

from app.db.serializer import cs_str
from app.db.utils import (
    DESC_PREFIX,
    OPERATOR_SPLITTER,
    OPERATORS,
    classproperty,
    has_operator_splitter,
)


class InspectionMixin(object):
    @classproperty
    def relations(cls) -> list:
        """Return a `list` of relationship names or the given model"""
        return [
            c.key
            for c in cls.__mapper__.iterate_properties  # type: ignore
            if isinstance(c, RelationshipProperty)
        ]


class FilterSortMixin(object):
    @classmethod
    def filter_expr(cls: Type, **filters: Any) -> list:
        if issubclass(cls, AliasedClass):
            mapper, _ = cls, inspect(cls).mapper.class_
        else:
            mapper = cls

        expressions = []
        for attr, value in filters.items():
            if has_operator_splitter(attr):
                attr_name, op_name = attr.rsplit(OPERATOR_SPLITTER, 1)
                op = OPERATORS[op_name]
            else:
                attr_name, op = attr, operators.eq

            column = getattr(mapper, attr_name)
            if isinstance(value, cs_str):
                values = value.split(",")
                expressions.append(sql_operators.in_op(column, values))
            else:
                expressions.append(op(column, value))

        return expressions

    @classmethod
    def order_expr(cls: Type, *columns: str) -> list:
        if issubclass(cls, AliasedClass):
            mapper, _ = cls, inspect(cls).mapper.class_
        else:
            mapper = cls

        expressions = []

        for attr in columns:
            fn, attr = (desc, attr[1:]) if attr.startswith(DESC_PREFIX) else (asc, attr)

            expr = fn(getattr(mapper, attr))
            expressions.append(expr)

        return expressions

    @classmethod
    def get_model_columns(cls) -> Dict[str, str]:
        return get_columns(cls).keys()
