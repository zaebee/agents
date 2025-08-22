from abc import ABC, abstractmethod
from typing import Tuple, TypeVar, Generic
from .periodic_table import ElementSymbol

# --- Generic TypeVars ---
TCommand = TypeVar("TCommand")
TEvent = TypeVar("TEvent")
TData = TypeVar("TData")
TDTO = TypeVar("TDTO")
TExternalInput = TypeVar("TExternalInput")
TExternalOutput = TypeVar("TExternalOutput")

# --- Base Classes ---

class Primitive(ABC):
    """Base class for all Hive primitives (like an atom)."""
    @property
    @abstractmethod
    def symbol(self) -> ElementSymbol:
        """The element's symbol (e.g., A for Aggregate)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def valency(self) -> Tuple[int, int]:
        """Input/output valency (e.g., (1, 1) for Aggregate)."""
        raise NotImplementedError

class Aggregate(Primitive, Generic[TCommand, TEvent], ABC):
    @property
    def symbol(self) -> ElementSymbol:
        return ElementSymbol.A

    @property
    def valency(self) -> Tuple[int, int]:
        return (1, 1)

    @abstractmethod
    def handle(self, command: TCommand) -> TEvent: ...

class Transform(Primitive, Generic[TData, TDTO], ABC):
    @property
    def symbol(self) -> ElementSymbol:
        return ElementSymbol.T

    @property
    def valency(self) -> Tuple[int, int]:
        return (1, 1)

    @abstractmethod
    def execute(self, data: TData) -> TDTO: ...

class Connector(Primitive, Generic[TExternalInput, TExternalOutput], ABC):
    @property
    def symbol(self) -> ElementSymbol:
        return ElementSymbol.C

    @property
    def valency(self) -> Tuple[int, int]:
        return (1, 1)

    @abstractmethod
    def process(self, input_data: TExternalInput) -> TExternalOutput: ...
