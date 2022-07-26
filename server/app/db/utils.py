import operator as operators_orig
import re
from collections import OrderedDict
from datetime import date, datetime
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Type,
    Union,
    cast,
)

from sqlalchemy import Column, Table, any_, func, or_
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session, aliased
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.sql import Select, operators
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy_utils import get_mapper

from app.exceptions.custom import InvalidDateFormat

if TYPE_CHECKING:
    from app.db.base_class import Base
    from app.db.filters import BaseSort, FilterType

RELATION_SPLITTER = "___"
OPERATOR_SPLITTER = "__"
DESC_PREFIX = "-"

OPERATORS: Dict[str, Callable] = {
    "isnull": lambda c, v: c.is_(None),
    "isnotnull": lambda c, v: c.isnot(None),
    "exact": operators_orig.eq,
    "ne": operators_orig.ne,  # not equal or is not (for None)
    "gt": operators_orig.gt,  # greater than , >
    "gte": operators_orig.ge,  # greater than or equal, >=
    "lt": operators_orig.lt,  # lower than, <
    "lte": operators_orig.le,  # lower than or equal, <=
    "like": operators.like_op,
    "ilike": operators.ilike_op,
    "startswith": operators.startswith_op,
    "istartswith": lambda c, v: c.ilike(v + "%"),
    "endswith": operators.endswith_op,
    "iendswith": lambda c, v: c.ilike("%" + v),
    "contains": lambda c, v: c.ilike("%{v}%".format(v=v)),
    "notlike": lambda c, v: c.not_like("%{v}%".format(v=v)),
    "asdate": lambda c, v: func.date(c) == v,
    "asdate_ne": lambda c, v: func.date(c) != v,
    "asdate_gt": lambda c, v: func.date(c) > v,
    "asdate_ge": lambda c, v: func.date(c) >= v,
    "asdate_lt": lambda c, v: func.date(c) < v,
    "asdate_le": lambda c, v: func.date(c) <= v,
    "in": lambda c, v: c.in_(v),
    "notin": lambda c, v: c.notin_(v),
    "notin_or_isnull": lambda c, v: or_(c.notin_(v), c.is_(None)),
    "any": lambda c, v: c == any_(func.array(v)),
}


def has_relation_splitter(val: str) -> bool:
    return re.search(rf"[a-z]+{RELATION_SPLITTER}[a-z]+", val) is not None


def has_operator_splitter(val: str) -> bool:
    return re.search(rf"[a-z]+{OPERATOR_SPLITTER}[a-z]+", val) is not None


class classproperty(object):
    """
    @property for @classmethod
    taken from http://stackoverflow.com/a/13624858
    """

    def __init__(self, fget: Any) -> None:
        self.fget = fget

    def __get__(self, owner_self: Any, owner_cls: Any) -> Any:
        return self.fget(owner_cls)


def _parse_path_and_make_aliases(
    entity: Union[AliasedClass, "Type[Base]"],
    entity_path: str,
    attrs: list,
    aliases: OrderedDict,
) -> None:
    """
    Sample values:
    attrs: ['product__subject_ids', 'user_id', '-group_id',
            'user__name', 'product__name', 'product__grade_from__order']
    relations: {'product': ['subject_ids', 'name'], 'user': ['name']}
    """
    relations: Dict[str, List[str]] = {}
    # take only attributes that have magic RELATION_SPLITTER
    for attr in attrs:
        # from attr (say, 'product__grade__order')  take
        # relationship name ('product') and nested attribute ('grade__order')
        if has_relation_splitter(attr):
            relation_name, nested_attr = attr.split(RELATION_SPLITTER, 1)
            if relation_name in relations:
                relations[relation_name].append(nested_attr)
            else:
                relations[relation_name] = [nested_attr]

    for relation_name, nested_attrs in relations.items():
        path = (
            entity_path + RELATION_SPLITTER + relation_name
            if entity_path
            else relation_name
        )
        if relation_name not in entity.relations:
            raise KeyError(
                "Incorrect path `{}`: "
                "{} doesnt have `{}` relationship ".format(path, entity, relation_name)
            )
        relationship = getattr(entity, relation_name)
        alias = aliased(relationship.property.mapper.class_)
        aliases[path] = alias, relationship
        _parse_path_and_make_aliases(alias, path, nested_attrs, aliases)


def _get_root_cls(query: Select) -> "Type[Base]":
    if hasattr(query, "columns_clause_froms"):
        if isinstance(getattr(query, "columns_clause_froms")[0], Table):
            return get_mapper(getattr(query, "columns_clause_froms")[0]).class_

    if hasattr(query, "_raw_columns"):
        return get_mapper(getattr(query, "_raw_columns")[0]).class_

    if hasattr(query, "_from_obj"):
        return get_mapper(getattr(query, "_from_obj")[0]).class_

    if hasattr(query, "_entity_from_pre_ent_zero"):
        return getattr(query, "_entity_from_pre_ent_zero")().class_

    raise ValueError(f"Cannot get a root class from`{query}`")


def _get_python_type_from_column(column: Column) -> type:
    return column.type.python_type


def _cast_to_datetime(val: str) -> datetime:
    try:
        return datetime.strptime(val, "%Y-%m-%d %H:%M")
    except ValueError:
        try:
            return datetime.strptime(val, "%Y-%m-%d")
        except ValueError:
            raise InvalidDateFormat(
                "Invalid date format. Supported date formats are "
                "YYYY-MM-DD or YYYY-MM-DD HH:mm"
            )


def _cast_to_date(val: str) -> date:
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except ValueError:
        raise InvalidDateFormat("Invalid date format" "YYYY-MM-DD format is required")


def _cast_value_to_type(val: Any, _type: type) -> Any:
    if type(val) == _type:
        return val

    if isinstance(val, str) and _type != str:
        if _type == datetime:
            return _cast_to_datetime(val)
        elif _type == date:
            return _cast_to_date(val)
        else:
            return _type(val)  # Cast value

    return val


def _add_filters_and_sort_to_query(
    query: Select,
    entity: "Type[Base]",
    aliases: dict,
    filters: dict,
    sort_attrs: List[str],
) -> Select:
    """Adds filters and sort attributes to a query"""
    for key, val in filters.items():
        col1 = key

        if has_relation_splitter(col1):
            parts = col1.rsplit(RELATION_SPLITTER, 1)
            temp_entity, attr_name = aliases[parts[0]][0], parts[1]
        else:
            temp_entity, attr_name = entity, key

        temp_name = attr_name
        if has_operator_splitter(temp_name):
            temp_name, _ = temp_name.rsplit(OPERATOR_SPLITTER, 1)
        column = getattr(temp_entity, temp_name)
        python_type = _get_python_type_from_column(column)
        cast_value = _cast_value_to_type(val, python_type)

        # if has_operator_splitter(key) and key != attr_name:
        #     attr_name = key
        try:
            query = query.where(*temp_entity.filter_expr(**{attr_name: cast_value}))
        except KeyError as e:
            raise KeyError(f"Incorrect filter path: `{col1}`: {e}")

    for attr in sort_attrs:
        if RELATION_SPLITTER in attr:
            prefix = ""
            if attr.startswith(DESC_PREFIX):
                prefix = DESC_PREFIX
                attr = attr.lstrip(DESC_PREFIX)
            parts = attr.rsplit(RELATION_SPLITTER, 1)
            temp_entity, attr_name = aliases[parts[0]][0], prefix + parts[1]
        else:
            temp_entity, attr_name = entity, attr

        try:
            query = query.order_by(*temp_entity.order_expr(attr_name))
        except KeyError as e:
            raise KeyError("Incorrect order path `{}`: {}".format(attr, e))

    return query


def _create_filtered_query_from_query(
    *,
    query: Select,
    filters: dict,
    sort_attrs: Optional[List[str]] = None,
    sort: bool = True,
    sorting_pk: Optional[str] = None,
    entity: Optional[Type["Base"]] = None,
) -> Select:
    if not sort_attrs:
        if sort:
            sort_attrs = ["-created_at"]
            if sorting_pk:
                sort_attrs.append(sorting_pk)
        else:
            sort_attrs = []
    else:
        if sorting_pk:
            sort_attrs.append(sorting_pk)

    if not entity:
        entity = _get_root_cls(query)
    attrs = list(filters.keys()) + [attr.lstrip(DESC_PREFIX) for attr in sort_attrs]
    aliases: OrderedDict[str, list] = OrderedDict({})
    _parse_path_and_make_aliases(entity, "", attrs, aliases)

    loaded_paths = []
    # Join necessary tables
    for path, al in aliases.items():
        relationship_path = path.replace(RELATION_SPLITTER, ".")
        query = query.outerjoin(al[0], al[1])
        loaded_paths.append(relationship_path)

    # Add filters and sort attributes
    query = _add_filters_and_sort_to_query(
        query,
        entity,
        aliases,
        filters,
        sort_attrs,
    )

    return query


def strip_operator(string: str) -> str:
    if re.search(r"[a-z]+__[a-z]+", string):
        return string.rsplit(OPERATOR_SPLITTER, 1)[0]
    return string


def fields_list_to_dict(fields_list: List[str]) -> Dict[str, Any]:
    fields_dict: Dict[str, Any] = {}
    for field in fields_list:
        field_name, value = field.split("=")
        fields_dict[field_name] = value

    return fields_dict


def to_timestamp(dt: datetime) -> int:
    return round(dt.timestamp())


def datetime_le(column: Column, other: Union[datetime, date]) -> BooleanClauseList:
    if isinstance(other, datetime):
        return or_(column < other, column == other)

    return or_(func.date(column) < other, func.date(column) == other)


def datetime_ge(column: Column, other: Union[datetime, date]) -> BooleanClauseList:
    if isinstance(other, datetime):
        return or_(column > other, column == other)

    return or_(func.date(column) > other, func.date(column) == other)


def parse_query_filters(filters: Optional[Union["FilterType", dict]] = None) -> dict:
    filters_dict = {}
    if filters:
        if isinstance(filters, dict):
            filters_dict = {key: val for key, val in filters.items() if val is not None}
        else:
            filters_dict = filters.dict(exclude_unset=True)
    return filters_dict


def filter_by_date(
    date_column: Column,
    query: Select,
    start_date: datetime,
    end_date: datetime,
) -> Select:
    more_than_1_day = start_date.date() != end_date.date()
    if not more_than_1_day:
        query = query.where(func.date(date_column) == start_date.date())
    else:
        query = query.where(datetime_ge(date_column, start_date.date())).filter(
            datetime_le(date_column, end_date.date())
        )

    return query


def sort_enum_to_str(sort_enum: "BaseSort") -> str:
    value = sort_enum.value
    aliases = sort_enum.get_aliases()
    is_desc = False

    if value.startswith(DESC_PREFIX):
        is_desc = True
        value = value[1:]

    if value in aliases:
        return "-" + aliases[value] if is_desc else aliases[value]

    return "-" + value if is_desc else value


# Recipe got from
# https://github.com/sqlalchemy/sqlalchemy/wiki/RangeQuery-and-WindowedRangeQuery
def _yield_limit(
    db: Session,
    qry: Select,
    pk_attr: Column,
    maxrq: int = 100,
    is_model_obj: bool = True,
) -> Generator:
    """specialized windowed query generator (using LIMIT/OFFSET)

    This recipe is to select through a large number of rows thats too
    large to fetch at once. The technique depends on the primary key
    of the FROM clause being an integer value, and selects items
    using LIMIT."""
    first_pks = set()
    first_pk: Optional[str] = None
    while True:
        q = qry
        if first_pk is not None:
            if first_pk in first_pks:
                break
            first_pks.add(first_pk)
            q = qry.where(pk_attr > first_pk)
        rec: Optional[Union[Row, Base]] = None

        for rec in db.execute(q.order_by(pk_attr).limit(maxrq)).unique():
            if is_model_obj:
                yield rec[0]
            else:
                yield rec

        if rec is None:
            break  # type: ignore [unreachable]

        if is_model_obj:
            rec = rec[0]

        if is_model_obj:
            first_pk = pk_attr.__get__(rec, pk_attr) if rec else None
        else:
            # Row objects have an '_asdict` method which converts a
            # row to a dict
            rec = cast(Row, rec)
            rec_dict = rec._asdict()
            first_pk = rec_dict[pk_attr.name] if rec else None


def dict_to_colon_str(d: dict) -> str:
    return ":".join([f"{key}:{d[key]}" for key in sorted(d.keys())])
