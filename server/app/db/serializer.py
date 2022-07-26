import re
from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, Generator, List, Optional, Type, cast, get_origin

from pydantic import Field, ValidationError, validator
from pydantic.fields import ModelField
from pydantic.main import BaseModel
from pydantic.utils import GetterDict
from sqlalchemy.exc import InvalidRequestError, MissingGreenlet

from app.db.pagination import Page
from app.db.utils import OPERATOR_SPLITTER, OPERATORS
from app.exceptions.custom import HttpErrorException
from app.utils.fns import convert_utc_to_timezone_date


class LazyAwareGetterDict(GetterDict):
    """
    This class captures lazy loads and exposes the
    offending attributes in a cleaner way
    """

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return super(LazyAwareGetterDict, self).get(key, default)
        except (MissingGreenlet, InvalidRequestError):
            raise AttributeError(f"Attribute '{key}' is being lazily loaded.")


class TrimmableBaseModel(BaseModel):
    def __init__(self, **data: Any) -> None:
        try:
            super().__init__(**data)
        except ValidationError as e:
            for error in e.errors():
                # Any other error type should rethrow the validation error
                if error["type"] != "value_error.missing":
                    raise e

    @classmethod
    def fields(cls) -> list:
        out = []

        def flatten(obj: Dict[str, ModelField], name: str = "") -> None:
            for key, val in obj.items():
                if get_origin(val.outer_type_) == list and issubclass(
                    val.type_, BaseModel
                ):
                    key = f"{key}[]"
                if issubclass(val.type_, BaseModel):
                    flatten(val.type_.__fields__, f"{name}{key}.")
                else:
                    out.append(name + key)

        flatten(cls.__fields__)
        return out


class InDBBaseSerializer(BaseModel):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime]

    @validator("updated_at")
    def default_updated_at_to_created_at(
        cls, updated_at: Optional[datetime], values: Dict
    ) -> datetime:
        if not updated_at:
            updated_at = (
                values["created_at"] if values["created_at"] else datetime.now()
            )
        return convert_utc_to_timezone_date(updated_at)

    @validator("created_at")
    def format_created_at_to_request_timezone(cls, created_at: datetime) -> datetime:
        return convert_utc_to_timezone_date(created_at)

    class Config:
        orm_mode = True
        getter_dict = LazyAwareGetterDict


class TrimmableInDBBaseSerializer(TrimmableBaseModel):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime]

    @validator("updated_at")
    def default_updated_at_to_created_at(
        cls, updated_at: Optional[datetime], values: Dict
    ) -> datetime:
        if not updated_at:
            updated_at = (
                values["created_at"] if values["created_at"] else datetime.now()
            )
        return convert_utc_to_timezone_date(updated_at)

    @validator("created_at")
    def format_created_at_to_request_timezone(cls, created_at: datetime) -> datetime:
        return convert_utc_to_timezone_date(created_at)

    class Config:
        orm_mode = True
        getter_dict = LazyAwareGetterDict


class InDBLiteSerializer(BaseModel):
    id: str

    class Config:
        orm_mode = True
        getter_dict = LazyAwareGetterDict


class TrimmableInDBLiteSerializer(TrimmableBaseModel):
    id: str

    class Config:
        orm_mode = True
        getter_dict = LazyAwareGetterDict


class SearchParam(BaseModel):
    q: Optional[str]


class Empty(BaseModel):
    pass


class NameSerializer(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True
        getter_dict = LazyAwareGetterDict


class ExportParam(BaseModel):
    get_export_fields: Optional[bool] = False
    export_fields: Optional[str] = ""


class cs_str(str):  # comma separated string
    @classmethod
    def __get_validators__(cls) -> Generator:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> "cs_str":
        if not isinstance(v, str):
            raise TypeError("string required")

        return cls(v)

    def __repr__(self) -> str:
        return f"cs_str({super().__repr__()})"


class ComplexFilter(str):
    @classmethod
    def __get_validators__(cls) -> Generator:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> "ComplexFilter":
        if not isinstance(v, str):
            raise TypeError("string required")

        parts = [field.strip(" ") for field in v.split(",")]
        for part in parts:
            if "=" not in part:
                raise ValueError("'=' must be present in field")

            if OPERATOR_SPLITTER in part:
                field, value = part.split("=")
                field_name, op = field.split(OPERATOR_SPLITTER)

                if op not in OPERATORS:
                    raise ValueError(f"'{op}' is not a valid operator")

        return cls(v)

    def __repr__(self) -> str:
        return f"ComplexFilter({super().__repr__()})"


def is_trimmable_serializer(model: Type[BaseModel]) -> bool:
    # Check for paged objects
    if issubclass(model, Page):
        return issubclass(model.__fields__["items"].type_, TrimmableBaseModel)

    return issubclass(model, TrimmableBaseModel)


def is_page_serializer(model: Type[BaseModel]) -> bool:
    return issubclass(model, Page)


def get_trimmable_fields(model: Type[BaseModel]) -> list:
    if is_trimmable_serializer(model):
        if is_page_serializer(model):
            return model.__fields__["items"].type_.fields()

        return cast(TrimmableBaseModel, model).fields()

    return []


def fields_to_dict(fields: List[str]) -> dict:
    """
    This functions
    ['test', 'test2.name', 'test3[].name']
    to
    {
        'test': True,
        'test2': {
            'name': True
        },
        'test3': {
            '__all__': {
                'name': True,
            }
        }
    }
    """
    out: dict = {}

    def unflatten(_fields: List[str], _dict: dict) -> None:
        for field in _fields:
            if "." in field:
                key, other = field.split(".", maxsplit=1)
                is_list = False
                if key.endswith("[]"):
                    key = key[:-2]
                    is_list = True

                if key not in _dict:
                    if is_list:
                        _dict[key] = {"__all__": {}}
                    else:
                        _dict[key] = {}

                if is_list:
                    unflatten([other], _dict[key]["__all__"])
                else:
                    unflatten([other], _dict[key])
            else:
                _dict[field] = True

    unflatten(fields, out)
    return out


class TrimHandler:
    def __init__(self, model: Type[BaseModel], fields: List[str]) -> None:
        self.fields = fields
        self.model = model

    def get_fields_to_return(self) -> dict:
        trimmable_fields = set(get_trimmable_fields(self.model))
        fields_to_return = set()
        for field in self.fields:
            for field_from_serializer in trimmable_fields:
                try:
                    if re.match(field, field_from_serializer):
                        fields_to_return.add(field_from_serializer)
                except re.error:
                    raise HttpErrorException(
                        status_code=HTTPStatus.BAD_REQUEST,
                        error_code="INVALID REGEX",
                        error_message="INVALID REGEX ON {}".format(field),
                    )

        if is_page_serializer(self.model):
            return {
                "items": {"__all__": fields_to_dict(list(fields_to_return))},
                "total": True,
                "current_page": True,
                "next_page": True,
                "total_pages": True,
            }
        else:
            return fields_to_dict(list(fields_to_return))
