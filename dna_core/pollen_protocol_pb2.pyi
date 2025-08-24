import datetime

from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PollenEnvelope(_message.Message):
    __slots__ = (
        "event_id",
        "event_type",
        "event_version",
        "timestamp",
        "aggregate_id",
        "payload",
    )
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EVENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    event_type: str
    event_version: str
    timestamp: _timestamp_pb2.Timestamp
    aggregate_id: str
    payload: _struct_pb2.Struct
    def __init__(
        self,
        event_id: _Optional[str] = ...,
        event_type: _Optional[str] = ...,
        event_version: _Optional[str] = ...,
        timestamp: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        aggregate_id: _Optional[str] = ...,
        payload: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
    ) -> None: ...
