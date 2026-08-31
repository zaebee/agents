# Specialized expressions of the core primitives, born from Royal Jelly.

from .base import Aggregate, Transform
from typing import List

# --- Specialized Aggregates ---

class OrchestratorAggregate(Aggregate):
    """
    A specialized Aggregate that manages the state of a long-running
    process or "quest" (Saga). It is the heart of a Chronicler Bee.

    Its 'handle_command' method would typically involve looking up the
    current state of the quest and dispatching the next command in the
    sequence. Its state is the quest log itself.
    """
    @property
    def name(self) -> str:
        return "OrchestratorAggregate"

    @property
    def description(self) -> str:
        return "A stateful component that manages a long-running process (Saga)."

    def handle_command(self, command) -> List:
        # Implementation would involve a state machine based on the quest.yaml
        print(f"Orchestrator handling command: {command}")
        return []


class RouterAggregate(Aggregate):
    """
    A specialized Aggregate that manages the state of routing decisions.
    It is the heart of a "Gene Shaper" bee, used for canary testing
    or A/B testing of new components.

    Its 'handle_command' method would inspect the incoming command and,
    based on its internal routing rules (e.g., 95% to stable, 5% to mutant),
    it would produce an event directing the command to the appropriate
    downstream component.
    """
    @property
    def name(self) -> str:
        return "RouterAggregate"

    @property
    def description(self) -> str:
        return "A stateful component that routes commands based on defined rules."

    def handle_command(self, command) -> List:
        # Implementation would involve routing logic.
        print(f"Router handling command: {command}")
        return []


# --- Specialized Transform ---

class MonitorTransform(Transform):
    """
    A specialized Transform that observes a stream of Genesis Events
    and transforms them into metrics. This is the heart of the "Humean"
    aspect of our Hive, as it facilitates learning from the sensory
    experience of the system.
    """
    @property
    def name(self) -> str:
        return "MonitorTransform"

    @property
    def description(self) -> str:
        return "A stateless service that transforms event streams into metrics."

    def process(self, event_stream: List) -> Dict:
        # Implementation would involve counting, aggregating, and
        # calculating metrics from the events.
        print(f"Monitor processing {len(event_stream)} events...")
        metric = {"events_processed": len(event_stream)}
        return metric
