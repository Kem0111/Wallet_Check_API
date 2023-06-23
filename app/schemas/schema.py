from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseConfig, BaseModel
from pydantic.generics import GenericModel
from pydantic.utils import GetterDict
from sqlalchemy import inspect
from sqlalchemy.orm.attributes import instance_state

if TYPE_CHECKING:
    from pydantic.typing import (
        AbstractSetIntStr,
        DictStrAny as PydanticDictStrAny,
        MappingIntStrAny,
    )


DictStrAny = Dict[str, Any]
RouteReturnT = Dict[str, Any]


class ExcludeNone:
    def dict(
        self,
        *,
        include: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        exclude: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> PydanticDictStrAny:
        exclude_none = True

        return super(ExcludeNone, self).dict(  # type: ignore
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def json(
        self,
        *,
        include: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        exclude: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        encoder: Optional[Callable[[Any], Any]] = None,
        models_as_dict: bool = True,
        **dumps_kwargs: Any,
    ) -> str:
        exclude_none = True

        return super(ExcludeNone, self).json(  # type: ignore
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            encoder=encoder,
            models_as_dict=models_as_dict,
            **dumps_kwargs,
        )


DetailT = Union[
    str,
    List[str],
    List[DictStrAny],
    DictStrAny,
]
ErrorT = Union[
    str,
    List[str],
    List[DictStrAny],
    DictStrAny,
]
ResponseT = TypeVar("ResponseT", bound=Any)


class ApplicationResponse(ExcludeNone, GenericModel, Generic[ResponseT]):
    class Config:
        allow_population_by_field_name = True
        smart_union = True
        orm_mode = True

    ok: bool
    result: Optional[ResponseT] = None
    detail: Optional[DetailT] = None
    error: Optional[ErrorT] = None
    error_code: Optional[int] = None
