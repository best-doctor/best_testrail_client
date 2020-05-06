import typing
import typing_extensions

ModelID = int
FieldName = str
FieldValue = typing.Any
TimeStamp = int
DeleteResult = bool
TimeSpan = str

JsonData = typing.Dict[FieldName, FieldValue]

Method = typing_extensions.Literal['GET', 'POST']


class PaginatorFilters(typing_extensions.TypedDict, total=False):
    limit: typing.Optional[int]
    offset: typing.Optional[int]


class StatusFilters(PaginatorFilters, total=False):
    status_ids: typing.Optional[typing.List[ModelID]]


class CreatedFilters(StatusFilters, total=False):
    created_after: typing.Optional[TimeStamp]
    created_before: typing.Optional[TimeStamp]
    created_by: typing.Optional[typing.List[ModelID]]
