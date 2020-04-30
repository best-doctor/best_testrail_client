from __future__ import annotations

from best_testrail_client.custom_types import JsonData

if False:  # TYPE_CHECKING
    import typing

    BaseModelType = typing.TypeVar('BaseModelType', bound='BaseModel')


class BaseModel:
    def __init__(self, **kwargs: typing.Any):
        pass

    @classmethod
    def from_json(cls: typing.Type[BaseModelType], data_json: JsonData) -> BaseModelType:
        return cls(**data_json)
