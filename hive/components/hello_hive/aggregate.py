import uuid
from datetime import datetime, timezone
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp
from dna_core.pollen_protocol_pb2 import PollenEnvelope
from dna_core.royal_jelly import Aggregate
from .command import HelloHiveCommand


class HelloHiveAggregate(Aggregate):
    """
    The aggregate for the hello-hive component.
    It handles commands and produces events.
    """

    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
        # Initialize state attributes here, e.g., self.status = None

    def handle_command(self, command: HelloHiveCommand) -> None:
        """
        Handles the incoming command and records the resulting event.
        """
        # Business logic and validation would go here.

        # Create a Struct for the payload
        payload_struct = Struct()
        payload_struct.update(command.payload)

        # Create the PollenEnvelope
        timestamp = Timestamp()
        timestamp.FromDatetime(datetime.now(timezone.utc))

        event = PollenEnvelope(
            event_id=str(uuid.uuid4()),
            event_type="HelloHiveCreatedEvent",
            event_version="1.0",
            aggregate_id=self.id,
            timestamp=timestamp,
            payload=payload_struct,
        )
        self._record_event(event)

    def _apply_event(self, event: PollenEnvelope) -> None:
        """
        Applies an event to the aggregate's state.
        """
        if event.event_type == "HelloHiveCreatedEvent":
            # Update state based on the event payload
            # e.g., self.status = "CREATED"
            # To access payload data: dict(event.payload)
            print(f"Applied {event.event_type} to aggregate {self.id}")
        else:
            print(f"Warning: Unhandled event type {event.event_type}")
