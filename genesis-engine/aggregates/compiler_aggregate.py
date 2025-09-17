# The "Organ" of our Genesis Engine - The Compiler Aggregate

from dataclasses import dataclass, field
from typing import Dict, List, Any


# This would be a real, importable class from our dna-core library in a mature system
@dataclass
class HatchCommand:
    """A command to hatch a new component."""

    codon_type: str
    component_name: str


# This would also be a real, importable event class
@dataclass
class ComponentHatchingInitiated:
    """An event produced when a hatch command is successfully validated."""

    component_name: str
    component_path: str
    codon_type: str
    templates: List[str]
    event_type: str = field(default="ComponentHatchingInitiated", init=False)


class CompilerAggregate:
    """
    This aggregate manages the state of the component being built.
    Its primary job is to validate hatch commands and produce events.
    """

    # The "Genetic Map" defining which templates belong to which codon.
    CODON_BLUEPRINTS: Dict[str, List[str]] = {
        "command": ["C.py.tpl", "A.py.tpl", "G.py.tpl", "command.py.tpl"],
        "query": ["C.py.tpl", "T.py.tpl", "query.py.tpl", "dto.py.tpl"],
        "event": ["G.py.tpl", "C.py.tpl", "A.py.tpl", "command.py.tpl"],
        "immune": ["C.py.tpl", "immune.py.tpl", "command.py.tpl"],
    }

    def __init__(self):
        self._pending_events: List[Any] = []
        print("  - CompilerAggregate initialized.")

    def get_pending_events(self) -> List[Any]:
        """Returns the list of events produced since the last save."""
        return self._pending_events

    def handle_hatch_command(self, command: HatchCommand, hive_root: str) -> List[Any]:
        """
        Handles the generic hatch command using a data-driven approach.
        """
        print(f"  - CompilerAggregate handling '{command.codon_type}' hatch command...")

        # 1. Look up the required templates from our genetic map
        templates_to_use = self.CODON_BLUEPRINTS.get(command.codon_type)

        if not templates_to_use:
            raise ValueError(f"Unknown codon type: {command.codon_type}")

        # 2. If valid, create the event payload
        event = ComponentHatchingInitiated(
            component_name=command.component_name,
            component_path=f"{hive_root}/{command.component_name}",
            codon_type=command.codon_type,
            templates=templates_to_use,
        )

        # 3. Add to pending events
        self._pending_events.append(event)
        print(f"  - CompilerAggregate produced event: {event.event_type}")

        return self.get_pending_events()
