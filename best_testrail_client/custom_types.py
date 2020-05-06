import typing
import typing_extensions

ModelID = int
FieldName = str
FieldValue = typing.Any
TimeStamp = int
DeleteResult = bool

JsonData = typing.Dict[FieldName, FieldValue]

Method = typing_extensions.Literal['GET', 'POST']
