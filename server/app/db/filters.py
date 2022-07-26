import abc
from enum import Enum
from typing import Any, TypeVar

from pydantic import BaseModel, root_validator

from app.db.serializer import ComplexFilter
from app.db.utils import fields_list_to_dict


class BaseFilter(BaseModel, abc.ABC):
    class Config:
        underscore_attrs_are_private = True

    @root_validator(pre=True)
    def validate_fields(cls, values: dict) -> dict:
        for key, val in cls.__fields__.items():
            if val.type_ == ComplexFilter:
                if "allowed_fields" not in cls.schema()["properties"][key]:
                    raise AttributeError("'allowed_fields' attribute is missing.")

                if not isinstance(
                    cls.schema()["properties"][key]["allowed_fields"], list
                ):
                    raise AttributeError("'allowed_fields' must be a list.")

        return values

    def dict(
        self,
        *,
        include: Any = None,
        exclude: Any = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> dict:
        data = super(BaseFilter, self).dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

        for key, val in self.__fields__.items():
            if val.type_ == ComplexFilter and key in data and data[key]:
                chunks = [field.strip(" ") for field in data[key].split(",")]
                data.update(fields_list_to_dict(chunks))
                del data[key]

        for private_attr in self.__slots__:
            if getattr(self, private_attr, None) is not None:
                data[private_attr[1:]] = getattr(self, private_attr)

        return data


FilterType = TypeVar("FilterType", bound=BaseFilter)


class BaseSort(str, Enum):
    def get_aliases(self) -> dict:
        return {}
