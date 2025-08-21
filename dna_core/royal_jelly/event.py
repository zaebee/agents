import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any

@dataclass(frozen=True)
class GenesisEvent:
    """
    The base class for all events in the Hive, following the Pollen Protocol.
    This is an immutable data transfer object.
    """

    # Fields without default values must come first.
    aggregate_id: str
    """The ID of the aggregate that produced the event."""

    payload: Dict[str, Any]
    """The data specific to this event."""

    # Fields with default values follow.
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    """A unique identifier for this specific event instance."""

    event_version: str = "1.0"
    """The version of the event schema to handle evolution."""

    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    """The UTC timestamp of when the event occurred."""

    # This field is not part of the constructor.
    event_type: str = field(init=False)
    """A clear, past-tense name of the event (e.g., `OrderShipped`)."""

    def __post_init__(self):
        """
        Sets the event_type based on the class name.
        """
        # The __setattr__ is used here because the dataclass is frozen.
        # This is a common pattern for setting a field value in a frozen dataclass's __post_init__.
        object.__setattr__(self, 'event_type', self.__class__.__name__)
