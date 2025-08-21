from dna_core.royal_jelly import Aggregate, GenesisEvent
from .command import ${ClassName}Command
from .event import ${ClassName}CreatedEvent

class ${ClassName}Aggregate(Aggregate):
    """
    The aggregate for the ${ComponentName} component.
    It handles commands and produces events.
    """

    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
        # Initialize state attributes here, e.g., self.status = None

    def handle_command(self, command: ${ClassName}Command) -> None:
        """
        Handles the incoming command and records the resulting event.
        """
        # Business logic and validation would go here.
        # For example, check if the order can be created.

        event = ${ClassName}CreatedEvent(
            aggregate_id=self.id,
            payload=command.payload  # Or transform the payload as needed
        )
        self._record_event(event)

    def _apply_event(self, event: GenesisEvent) -> None:
        """
        Applies an event to the aggregate's state.
        """
        if isinstance(event, ${ClassName}CreatedEvent):
            # Update state based on the event payload
            # e.g., self.status = "CREATED"
            print(f"Applied {type(event).__name__} to aggregate {self.id}")
        else:
            print(f"Warning: Unhandled event type {type(event).__name__}")
