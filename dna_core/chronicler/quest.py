from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass(frozen=True)
class Action:
    """Represents a single action to be executed."""

    action: str
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Transition:
    """Represents a transition from one state to another."""

    to: str
    on: str


@dataclass(frozen=True)
class State:
    """Represents a single state in the quest's state machine."""

    name: str
    description: str = ""
    on_enter: List[Action] = field(default_factory=list)
    transitions: List[Transition] = field(default_factory=list)


@dataclass(frozen=True)
class Quest:
    """Represents a full quest definition, loaded from a YAML file."""

    quest_name: str
    initial_state: str
    states: Dict[str, State]
