import datetime

from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PollenEnvelope(_message.Message):
    __slots__ = ("event_id", "event_type", "event_version", "timestamp", "aggregate_id", "payload")
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
    def __init__(self, event_id: _Optional[str] = ..., event_type: _Optional[str] = ..., event_version: _Optional[str] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., aggregate_id: _Optional[str] = ..., payload: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class GenomeMessage(_message.Message):
    __slots__ = ("primitive_type", "purpose", "nectar_production_rate")
    PRIMITIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PURPOSE_FIELD_NUMBER: _ClassVar[int]
    NECTAR_PRODUCTION_RATE_FIELD_NUMBER: _ClassVar[int]
    primitive_type: str
    purpose: str
    nectar_production_rate: int
    def __init__(self, primitive_type: _Optional[str] = ..., purpose: _Optional[str] = ..., nectar_production_rate: _Optional[int] = ...) -> None: ...

class WaggleDanceEvent(_message.Message):
    __slots__ = ("source_hive_id", "source_component_id", "fitness_score", "fitness_delta", "genome")
    SOURCE_HIVE_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_COMPONENT_ID_FIELD_NUMBER: _ClassVar[int]
    FITNESS_SCORE_FIELD_NUMBER: _ClassVar[int]
    FITNESS_DELTA_FIELD_NUMBER: _ClassVar[int]
    GENOME_FIELD_NUMBER: _ClassVar[int]
    source_hive_id: str
    source_component_id: str
    fitness_score: float
    fitness_delta: float
    genome: GenomeMessage
    def __init__(self, source_hive_id: _Optional[str] = ..., source_component_id: _Optional[str] = ..., fitness_score: _Optional[float] = ..., fitness_delta: _Optional[float] = ..., genome: _Optional[_Union[GenomeMessage, _Mapping]] = ...) -> None: ...
