import os
from typing import Any, Mapping, Optional, Type

import sqlalchemy as sa
from sqlalchemy import DDL, MetaData, event
from sqlalchemy.future import Connection
from sqlalchemy.orm import Mapper
from sqlalchemy.sql import ColumnElement, Select
from sqlalchemy_searchable import (
    CreateSearchFunctionSQL,
    CreateSearchTriggerSQL,
    DropSearchFunctionSQL,
    DropSearchTriggerSQL,
    SearchManager,
    inspect_search_vectors,
    search_manager,
)

from app.db.utils import _get_root_cls


def search(
    query: Select,
    search_query: Optional[str],
    vector: Optional[ColumnElement] = None,
    sort: bool = False,
) -> Select:
    if not search_query or not search_query.strip():
        return query

    if vector is None:
        entity = _get_root_cls(query)
        search_vectors = inspect_search_vectors(entity)
        vector = search_vectors[0]

    query = query.where(vector.op("@@")(sa.func.parse_websearch(search_query)))
    if sort:
        query = query.order_by(
            sa.desc(sa.func.ts_rank_cd(vector, sa.func.parse_websearch(search_query)))
        )

    return query.params(term=search_query)


# SQLAlchemy 2.0 compatible version of
# https://github.com/kvesteri/sqlalchemy-searchable/blob/ea46ffa9901bafad6cade3dcbc67416c135ba45d/sqlalchemy_searchable/__init__.py#L346
def sync_trigger(
    conn: Connection,
    table_name: str,
    tsvector_column: str,
    indexed_columns: list,
    metadata: Optional[sa.MetaData] = None,
    options: Optional[Any] = None,
) -> None:
    if metadata is None:
        metadata = sa.MetaData()
    table = sa.Table(table_name, metadata, autoload_with=conn)
    params = dict(
        tsvector_column=getattr(table.c, tsvector_column),
        indexed_columns=indexed_columns,
        options=options,
        conn=conn,
    )
    classes = [
        DropSearchTriggerSQL,
        DropSearchFunctionSQL,
        CreateSearchFunctionSQL,
        CreateSearchTriggerSQL,
    ]
    for class_ in classes:
        sql = class_(**params)
        conn.exec_driver_sql(str(sql), sql.params)
    update_sql = table.update().values(
        {indexed_columns[0]: sa.text(indexed_columns[0])}
    )
    conn.execute(update_sql)


path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(path, "sql_search_expressions.sql")) as file:
    statements = file.read().split("\n\n")
    sql_expressions = [DDL(stmt) for stmt in statements]


# https://github.com/kvesteri/sqlalchemy-searchable/blob/ea46ffa9901bafad6cade3dcbc67416c135ba45d/sqlalchemy_searchable/__init__.py#L537
def make_searchable(
    metadata: MetaData,
    mapper: Type[Mapper] = sa.orm.mapper,
    manager: SearchManager = search_manager,
    options: Mapping = {},
) -> None:
    manager.options.update(options)
    event.listen(mapper, "instrument_class", manager.process_mapper)
    event.listen(mapper, "after_configured", manager.attach_ddl_listeners)

    for expression in sql_expressions:
        event.listen(metadata, "before_create", expression)
