import typing

ModelID = int
FieldName = str
FieldValue = typing.Any

JsonData = typing.Dict[FieldName, FieldValue]

Method = typing.Literal['GET', 'POST']
