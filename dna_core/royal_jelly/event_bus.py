from typing import Callable, List, Dict, Protocol
from dna_core.pollen_protocol_pb2 import PollenEnvelope

# A type hint for an event handler function
EventHandler = Callable[[PollenEnvelope], None]

class IEventBus(Protocol):
    """
    A Protocol for an event bus, defining the contract for publishing events
    and subscribing handlers to event types.

    This uses structural typing. Any class that implements these methods with the
    correct signatures will be considered a valid IEventBus.
    """

    def publish(self, event: PollenEnvelope) -> None:
        """Publishes an event to all registered handlers."""
        ...

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Subscribes a handler to a specific event type string."""
        ...

class EventBus(IEventBus):
    """
    A simple in-memory implementation of the IEventBus.
    It maintains a dictionary of event type strings to a list of handlers.
    """

    def __init__(self):
        self._handlers: Dict[str, List[EventHandler]] = {}

    def publish(self, event: PollenEnvelope) -> None:
        """
        Publishes an event by calling all handlers subscribed to its event_type string.
        """
        event_type_str = event.event_type
        if event_type_str in self._handlers:
            for handler in self._handlers[event_type_str]:
                try:
                    handler(event)
                except Exception as e:
                    # In a real application, you'd have more robust error handling/logging here.
                    print(f"Error handling event {event_type_str}: {e}")

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """
        Subscribes a handler to an event type string. If the event type is not
        already in the handlers' dictionary, it's added.
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
