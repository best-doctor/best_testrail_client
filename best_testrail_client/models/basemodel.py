from __future__ import annotations

from best_testrail_client.custom_types import JsonData

if False:  # TYPE_CHECKING
    from typing import TypeVar, Type, Any

    BaseModelType = TypeVar('BaseModelType', bound='BaseModel')


class BaseModel:
    def __init__(self, **kwargs: Any):
        pass

    @classmethod
    def from_json(cls: Type[BaseModelType], data_json: JsonData) -> BaseModelType:
        return cls(**data_json)
