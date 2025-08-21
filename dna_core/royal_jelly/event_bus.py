from typing import Callable, List, Dict, Type
from abc import ABC, abstractmethod
from .event import GenesisEvent

# A type hint for an event handler function
EventHandler = Callable[[GenesisEvent], None]

class IEventBus(ABC):
    """
    An interface for an event bus, defining the contract for publishing events
    and subscribing handlers to event types.
    """

    @abstractmethod
    def publish(self, event: GenesisEvent) -> None:
        """Publishes an event to all registered handlers."""
        pass

    @abstractmethod
    def subscribe(self, event_type: Type[GenesisEvent], handler: EventHandler) -> None:
        """Subscribes a handler to a specific event type."""
        pass

class EventBus(IEventBus):
    """
    A simple in-memory implementation of the IEventBus.
    It maintains a dictionary of event types to a list of handlers.
    """

    def __init__(self):
        self._handlers: Dict[Type[GenesisEvent], List[EventHandler]] = {}

    def publish(self, event: GenesisEvent) -> None:
        """
        Publishes an event by calling all handlers subscribed to its type.
        """
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    # In a real application, you'd have more robust error handling/logging here.
                    print(f"Error handling event {event_type.__name__}: {e}")

    def subscribe(self, event_type: Type[GenesisEvent], handler: EventHandler) -> None:
        """
        Subscribes a handler to an event type. If the event type is not
        already in the handlers' dictionary, it's added.
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
