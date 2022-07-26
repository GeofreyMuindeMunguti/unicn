from datetime import datetime
from http import HTTPStatus
from typing import (
    Any,
    Dict,
    Generator,
    Generic,
    List,
    Optional,
    Protocol,
    Sequence,
    Type,
    TypedDict,
    TypeVar,
    Union,
)

from fastapi_pagination.bases import AbstractPage
from pydantic import BaseModel
from sqlalchemy import Column, insert, inspect, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import LoaderCriteriaOption, Session, raiseload
from sqlalchemy.orm.strategy_options import Load, _UnboundLoad
from sqlalchemy.sql import Select
from sqlalchemy_utils import get_hybrid_properties

from app.db.base_class import Base, generate_uuid
from app.db.custom_search import search
from app.db.filters import BaseSort, FilterType
from app.db.pagination import Page, Pagination, PaginationQueryParams, paginate
from app.db.serializer import ExportParam, SearchParam
from app.db.utils import (
    _create_filtered_query_from_query,
    _yield_limit,
    parse_query_filters,
    sort_enum_to_str,
)
from app.exceptions.custom import (
    DaoException,
    HttpErrorException,
    InvalidStateException,
)

ModelType = TypeVar("ModelType", bound=Base)
CreateSerializer = TypeVar("CreateSerializer", bound=BaseModel)
UpdateSerializer = TypeVar("UpdateSerializer", bound=BaseModel)
Serializer = TypeVar("Serializer", bound=BaseModel)
LoadOption = Union[_UnboundLoad, LoaderCriteriaOption, Load]


class ChangeAttrState(TypedDict):
    before: Any
    after: Any


# Class that we can use to keep track of the changes in an object
ChangedObjState = Dict[str, ChangeAttrState]


class DaoInterface(Protocol[ModelType]):
    model: ModelType
    load_options: List[LoadOption]

    def create(self, db: Session, *, obj_in: CreateSerializer) -> ModelType:
        pass

    def on_relationship(
        self,
        db: Session,
        *,
        pk: str,
        values: dict,
        db_obj: Optional[ModelType] = None,
        create: bool = True,
    ) -> None:
        pass

    def on_unknown_field(
        self, db: Session, *, db_obj: ModelType, key: str, value: Any
    ) -> None:
        pass

    def get(
        self,
        db: Session,
        load_options: Optional[Sequence[LoadOption]] = None,
        **filters: Any,
    ) -> Optional[ModelType]:
        pass

    def get_not_none(
        self,
        db: Session,
        load_options: Optional[Sequence[LoadOption]] = None,
        **filters: Any,
    ) -> ModelType:
        pass

    def on_pre_create(
        self, db: Session, pk: str, values: dict, orig_values: dict
    ) -> None:
        pass

    def on_post_create(
        self, db: Session, db_obj: Union[ModelType, List[ModelType]]
    ) -> None:
        pass

    def on_pre_update(
        self, db: Session, db_obj: ModelType, values: dict, orig_values: dict
    ) -> None:
        pass

    def on_post_update(
        self, db: Session, db_obj: ModelType, changed: ChangedObjState
    ) -> None:
        pass

    def customize_query(self, query: Select, filters: dict) -> Select:
        pass

    def modify_load_options(
        self, filters: dict, load_options: List[LoadOption]
    ) -> None:
        pass


class RelationshipsDao(Generic[ModelType]):
    def __init__(self, model: ModelType, **kwargs: Any):
        super(RelationshipsDao, self).__init__(model, **kwargs)  # type: ignore [call-arg]

    def on_relationship(
        self,
        db: Session,
        *,
        pk: str,
        values: dict,
        db_obj: Optional[ModelType] = None,
        create: bool = True,
    ) -> None:
        pass

    def on_unknown_field(
        self, db: Session, *, db_obj: ModelType, key: str, value: Any
    ) -> None:
        pass


class CreateDao(Generic[ModelType, CreateSerializer]):
    def __init__(
        self,
        model: Type[ModelType],
        **kwargs: Any,
    ):
        super(CreateDao, self).__init__(model, **kwargs)  # type: ignore [call-arg]
        self.model = model

    def create(
        self: Union[Any, DaoInterface], db: Session, *, obj_in: CreateSerializer
    ) -> ModelType:
        obj_in_data = obj_in.dict(exclude_none=True)
        orig_data = obj_in_data.copy()

        relationship_fields = inspect(self.model).relationships.keys()

        for key in list(obj_in_data.keys()):
            if (
                isinstance(obj_in_data[key], list)
                or key in relationship_fields
                or obj_in_data[key] is None
                or key not in self.model.get_model_columns()
            ):
                del obj_in_data[key]

        try:
            obj_id = obj_in_data.pop("id", None) or generate_uuid()
            if hasattr(self, "on_pre_create"):
                self.on_pre_create(
                    db, pk=obj_id, values=obj_in_data, orig_values=orig_data
                )
            stmt = insert(self.model.__table__).values(id=obj_id, **obj_in_data)
            db.execute(stmt)

            if hasattr(self, "on_relationship"):
                self.on_relationship(db, pk=obj_id, values=orig_data)

            db.commit()

            db_obj = self.get_not_none(db, id=obj_id)
            return db_obj

        except IntegrityError:
            db.rollback()
            raise

    def on_pre_create(
        self, db: Session, pk: str, values: dict, orig_values: dict
    ) -> None:
        pass

    def on_post_create(
        self, db: Session, db_obj: Union[ModelType, List[ModelType]]
    ) -> None:
        pass


class UpdateDao(Generic[ModelType, UpdateSerializer]):
    def __init__(self, model: Type[ModelType], **kwargs: Any):
        self.model = model
        super(UpdateDao, self).__init__(model, **kwargs)  # type: ignore [call-arg]

    def update(
        self: Union[Any, DaoInterface],
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSerializer, Dict[str, Any]],
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if not update_data:
            raise HttpErrorException(
                status_code=HTTPStatus.BAD_REQUEST,
                error_code="NO UPDATE DATA",
                error_message="No data was passed on update!",
            )

        if "created_at" in update_data:
            del update_data["created_at"]

        if not hasattr(db_obj, "updated_at"):
            update_data["updated_at"] = datetime.now()

        hybrid_property_fields = get_hybrid_properties(self.model).keys()
        relationship_fields = inspect(self.model).relationships.keys()

        orig_update_data = update_data.copy()

        for key in list(update_data.keys()):
            if (
                key in hybrid_property_fields
                or key in relationship_fields
                or key not in db_obj.get_model_columns()
                or update_data[key] is None
            ):
                del update_data[key]

        self.on_pre_update(
            db=db, db_obj=db_obj, values=update_data, orig_values=orig_update_data
        )
        # We need to keep track of attributes we are about to change
        changed_obj_state: ChangedObjState = {}
        for key in list(update_data.keys()):
            if key == "updated_at":
                continue

            if key in db_obj.get_model_columns():
                # Field has the same values, so we delete it
                if update_data[key] == getattr(db_obj, key):
                    del update_data[key]
                # Field has changed, so we track it
                else:
                    changed_obj_state[key] = {
                        "before": getattr(db_obj, key),
                        "after": update_data[key],
                    }

        stmt = (
            update(self.model.__table__)
            .where(self.model.id == db_obj.id)
            .values(**update_data)
            .execution_options(synchronize_session="evaluate")
        )
        db.execute(stmt)

        if hasattr(self, "on_relationship"):
            self.on_relationship(
                db, pk=db_obj.id, values=orig_update_data, db_obj=db_obj, create=False
            )
        try:
            db.commit()

            updated_db_obj = self.get_not_none(db, id=db_obj.id)

            return updated_db_obj
        except IntegrityError:
            db.rollback()
            raise

    def on_pre_update(
        self, db: Session, db_obj: ModelType, values: dict, orig_values: dict
    ) -> None:
        pass

    def on_post_update(
        self, db: Session, db_obj: ModelType, changed: ChangedObjState
    ) -> None:
        pass


class TransitionDao(Generic[ModelType]):
    """
    This dao method is called on_pre_update
    to validate state transitions.<
    """

    def __init__(
        self,
        model: Type[ModelType],
        *,
        state_transition_graph: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        self.model = model
        self.state_transition_graph = state_transition_graph

        if not self.state_transition_graph:
            self.state_transition_graph = state_transition_graph

    def validate_state_transition(self, *, db_obj: ModelType, values: dict) -> None:
        if self.state_transition_graph:
            state_key = self.state_transition_graph["key"]
        else:
            return

        if state_key not in values.keys():
            return

        transition_states: Dict[str, List] = self.state_transition_graph["graph"]
        possible_transitions = transition_states.get(
            db_obj.__getattribute__(str(state_key))
        )

        if possible_transitions:
            if values[state_key] not in possible_transitions:
                raise DaoException(
                    resource=f"{self.model}", message="State transition not permitted"
                )
        else:
            raise DaoException(
                resource=f"{self.model}",
                message="Transition graph for specified state not specified.",
            )


class DeleteDao(Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
        **kwargs: Any,
    ):
        super(DeleteDao, self).__init__(model, **kwargs)  # type: ignore [call-arg]
        self.model = model

    def remove(self, db: Session, *, id: str) -> Optional[ModelType]:
        obj = db.get(self.model, id)
        db.delete(obj)
        db.commit()
        return obj


class ReadDao(Generic[ModelType, Pagination]):
    def __init__(
        self,
        model: Type[ModelType],
        *,
        load_options: Optional[List[LoadOption]] = None,
        **kwargs: Any,
    ):
        super(ReadDao, self).__init__(model, **kwargs)  # type: ignore [call-arg]
        self.model = model
        self.load_options: Sequence
        if load_options is None:
            self.load_options = [raiseload("*", sql_only=True)]
        else:
            self.load_options = load_options + [raiseload("*", sql_only=True)]

        self.sorting_pk = "id"

    def reset_sorting_pk(self) -> None:
        self.sorting_pk = "id"

    def get(
        self: Union[Any, DaoInterface],
        db: Session,
        load_options: Optional[Sequence[LoadOption]] = None,
        **filters: Any,
    ) -> Optional[ModelType]:

        filters_dict = parse_query_filters(filters)
        query = select(self.model)
        query = self.customize_query(query, filters_dict)
        query = _create_filtered_query_from_query(query=query, filters=filters_dict)

        load_options = list(load_options or self.load_options)

        # TODO: Check for the presence of raiseload before adding
        load_options.append(raiseload("*", sql_only=True))
        if load_options:
            self.modify_load_options(filters_dict, load_options)
            query = query.options(*load_options)

        return db.scalars(query.limit(1)).first()

    def get_not_none(
        self,
        db: Session,
        load_options: Optional[Sequence[LoadOption]] = None,
        **filters: Any,
    ) -> ModelType:
        obj = self.get(db, load_options=load_options, **filters)
        if not obj:
            raise InvalidStateException(f"obj with filters {filters} not found")
        return obj

    def get_all(
        self,
        db: Session,
        *,
        load_options: Optional[Sequence[LoadOption]] = None,
        filters: Optional[Union[FilterType, Dict[str, Any]]] = None,
        sorting_fields: Optional[Sequence[BaseSort]] = None,
    ) -> List[ModelType]:
        sort_attrs = []
        if sorting_fields:
            sort_attrs = [sort_enum_to_str(field) for field in sorting_fields]

        filters_dict = parse_query_filters(filters)

        query = select(self.model)
        query = self.customize_query(query, filters_dict)
        query = _create_filtered_query_from_query(
            query=query, filters=filters_dict, sort_attrs=sort_attrs
        )
        load_options = list(load_options or self.load_options)

        # TODO: Check for the presence of raiseload before adding
        load_options.append(raiseload("*", sql_only=True))
        if load_options:
            self.modify_load_options(filters_dict, load_options)
            query = query.options(*load_options)
        return db.scalars(query).unique().all()

    def get_all_in_chunks(
        self,
        db: Session,
        *,
        filters: Optional[Union[FilterType, Dict[str, Any]]] = None,
        sorting_fields: Optional[Sequence[BaseSort]] = None,
        chunk: int = 500,
    ) -> Generator[ModelType, None, None]:
        sort_attrs = []
        if sorting_fields:
            sort_attrs = [sort_enum_to_str(field) for field in sorting_fields]

        filters_dict = parse_query_filters(filters)

        query = select(self.model)
        query = self.customize_query(query, filters_dict)
        query = _create_filtered_query_from_query(
            query=query, filters=filters_dict, sort=False, sort_attrs=sort_attrs
        )
        if self.load_options:
            load_options = list(self.load_options)
            self.modify_load_options(filters_dict, load_options)
            query = query.options(*load_options)

        for obj in _yield_limit(db, query, self.model.id, maxrq=chunk):
            yield obj

    def get_by_ids(self, db: Session, *, ids: List[str]) -> List[ModelType]:
        query = select(self.model)
        if self.load_options:
            query = query.options(*self.load_options)
        return db.scalars(query.where(self.model.id.in_(ids))).unique().all()

    def get_multi_paginated(
        self,
        db: Session,
        params: PaginationQueryParams,
        filters: Optional[Union[FilterType, Dict[str, Any]]] = None,
        sorting_fields: Optional[Sequence[BaseSort]] = None,
        export: Optional[ExportParam] = None,
    ) -> Union[AbstractPage[ModelType], List[ModelType]]:
        sort_attrs = []
        if sorting_fields:
            sort_attrs = [sort_enum_to_str(field) for field in sorting_fields]

        filters_dict = parse_query_filters(filters)

        query = select(self.model)

        query = self.customize_query(query, filters_dict)
        query = _create_filtered_query_from_query(
            query=query,
            filters=filters_dict,
            sort_attrs=sort_attrs,
            sorting_pk=self.sorting_pk,
        )
        # In case it was changed
        self.reset_sorting_pk()
        # We need to store the total_query for later use during counting
        total_query = query
        if self.load_options:
            load_options = list(self.load_options)
            self.modify_load_options(filters_dict, load_options)
            query = query.options(*load_options)

        if export:
            return db.scalars(query).unique().all()
        else:
            return paginate(db, query, total_query=total_query, params=params)

    def search(
        self,
        db: Session,
        search_param: SearchParam,
        pagination: PaginationQueryParams,
        *,
        filters: Optional[Union[FilterType, Dict[str, Any]]] = None,
        sorting_fields: Optional[Sequence[BaseSort]] = None,
    ) -> AbstractPage[ModelType]:
        sort_attrs = []
        if sorting_fields:
            sort_attrs = [sort_enum_to_str(field) for field in sorting_fields]

        filters_dict = parse_query_filters(filters)

        query = select(self.model)
        query = self.customize_query(query, filters_dict)
        query = _create_filtered_query_from_query(
            query=query,
            filters=filters_dict,
            sort_attrs=sort_attrs,
            sorting_pk=self.sorting_pk,
        )
        # In case it was changed
        self.reset_sorting_pk()

        search_vector: List[Column] = []
        query = self.setup_search_query(query, search_vector)

        query = search(
            query, search_param.q, search_vector[0] if search_vector else None
        )

        # We need to store the total_query for later use during counting
        total_query = query

        if self.load_options:
            load_options = list(self.load_options)
            self.modify_load_options(filters_dict, load_options)
            query = query.options(*load_options)

        return paginate(db, query, total_query=total_query, params=pagination)

    def setup_search_query(self, query: Select, search_vector: list) -> Select:
        return query

    def customize_query(self, query: Select, filters: dict) -> Select:
        return query

    def exists(self, db: Session, id: str) -> bool:
        return (
            db.scalars(select(self.model.id).filter_by(id=id).limit(1)).first()
            is not None
        )

    def modify_load_options(
        self, filters: dict, load_options: List[LoadOption]
    ) -> None:
        pass


class CRUDDao(
    CreateDao[ModelType, CreateSerializer],
    UpdateDao[ModelType, UpdateSerializer],
    DeleteDao[ModelType],
    ReadDao[ModelType, Page[ModelType]],
    RelationshipsDao[ModelType],
    TransitionDao[ModelType],
):
    def __init__(
        self,
        model: Type[ModelType],
        *,
        load_options: Optional[List[LoadOption]] = None,
        state_transition_graph: Optional[Dict[str, Sequence[str]]] = None,
    ):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        super(CRUDDao, self).__init__(
            model,
            load_options=load_options,
            state_transition_graph=state_transition_graph,
        )
