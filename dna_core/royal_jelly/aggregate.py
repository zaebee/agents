from typing import List
from abc import ABC, abstractmethod
from dna_core.pollen_protocol_pb2 import PollenEnvelope

class Aggregate(ABC):
    """
    The base class for an Aggregate.
    Aggregates are the core of the domain model, encapsulating state and business logic.
    They process commands and produce events.
    """

    def __init__(self, aggregate_id: str):
        self.id = aggregate_id
        self._uncommitted_events: List[PollenEnvelope] = []

    def get_uncommitted_events(self) -> List[PollenEnvelope]:
        """Returns the list of events that have not yet been published."""
        return self._uncommitted_events

    def clear_uncommitted_events(self) -> None:
        """Clears the list of uncommitted events."""
        self._uncommitted_events = []

    def _record_event(self, event: PollenEnvelope) -> None:
        """
        Records a new event and applies it to the aggregate's state.
        This is the primary way the aggregate's state should change.
        """
        self._apply_event(event)
        self._uncommitted_events.append(event)

    @abstractmethod
    def _apply_event(self, event: PollenEnvelope) -> None:
        """
        Applies an event to the aggregate, mutating its state.
        This method should be implemented by each specific aggregate to handle
        the events relevant to it. It's the "when" part of event sourcing.

        Example:
        if isinstance(event, OrderCreatedEvent):
            self.status = "CREATED"
        """
        pass
