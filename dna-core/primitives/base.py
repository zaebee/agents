# The Royal Jelly of the Hive
# This module contains the foundational base classes for all primitives.

from abc import ABC, abstractmethod
from typing import List, Any, Dict

# --- Foundational Interfaces ---

class HivePrimitive(ABC):
    """
    The abstract base class for all primitives (A, T, C, G).
    It represents the very essence of being a part of the Hive's DNA.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """The unique name of this primitive within the Hive."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A human-readable description of the primitive's purpose."""
        pass


class Command:
    """A marker base class for all Command objects."""
    pass


class GenesisEvent:
    """A marker base class for all Genesis Event objects."""
    pass


# --- Core Primitives as Abstract Base Classes ---

class Aggregate(HivePrimitive):
    """
    The base class for all Aggregates (A).
    Aggregates are stateful and handle commands to enforce business rules.
    They are the only things that can produce Genesis Events.
    """
    @abstractmethod
    def handle_command(self, command: Command) -> List[GenesisEvent]:
        """Processes a command and returns a list of resulting events."""
        pass


class Transform(HivePrimitive):
    """
    The base class for all Transformations (T).
    Transforms are stateless services that contain domain logic which
    doesn't belong to a single aggregate.
    """
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Processes input data and returns a result without side effects."""
        pass
