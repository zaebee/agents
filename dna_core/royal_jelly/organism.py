import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Tuple

from .periodic_table import ElementSymbol
from .primitives import Primitive


# --- Anatomy Structures ---

@dataclass(frozen=True)
class Genome:
    """The bee's static, compile-time blueprint. Its unchanging soul."""
    primitive_type: ElementSymbol
    bonds_template: Tuple[str, ...]
    valency: Tuple[int, int]
    purpose: str


@dataclass
class Epigenome:
    """The bee's dynamic, runtime memory. How it learns and adapts."""
    engrams: Dict[str, Any] = field(default_factory=dict)
    trust_network: Dict[str, float] = field(default_factory=dict)
    lineage: Dict[str, Any] = field(default_factory=dict)
    lore_adopted: List[str] = field(default_factory=list)


class HealthStatus(Enum):
    """The current health state of a digital organism."""
    HEALTHY = auto()
    STARVING = auto()
    TOXIC = auto()
    HIBERNATING = auto()


@dataclass
class Metabolism:
    """Governs the bee's energy, health, and emotional state."""
    nectar_level: int = 100
    health_status: HealthStatus = HealthStatus.HEALTHY
    age: int = 0
    affective_state: Dict[str, int] = field(
        default_factory=lambda: {"pain": 0, "joy": 0, "fear": 0}
    )


class LifecycleState(Enum):
    """The current stage in the bee's life journey."""
    NASCENT = auto()
    ACTIVE = auto()
    HIBERNATING = auto()
    DYING = auto()
    DECEASED = auto()


# --- The Unified Organism Class ---

class DigitalOrganism(Primitive, ABC):
    """
    The unified base class for all life in the Hive.
    It combines a static Genome with dynamic Epigenome, Metabolism, and Lifecycle.
    It inherits from Primitive to be a first-class citizen in the Hive's type system.
    """

    def __init__(self, genome: Genome):
        # The Unchanging Soul
        self.genome: Genome = genome
        self.id: str = f"{genome.primitive_type.name}-{uuid.uuid4()}"

        # The Learned Memory
        self.epigenome: Epigenome = Epigenome()

        # The Spark of Life
        self.metabolism: Metabolism = Metabolism()

        # The Dance of Existence
        self.lifecycle_state: LifecycleState = LifecycleState.NASCENT
        self.event_log: List[Any] = []  # To be replaced with GenesisEvent

    @property
    def symbol(self) -> ElementSymbol:
        """The element's symbol, inherited from the Genome."""
        return self.genome.primitive_type

    @property
    def valency(self) -> Tuple[int, int]:
        """Input/output valency, inherited from the Genome."""
        return self.genome.valency

    def tick(self):
        """
        The heartbeat of the bee. Called once per simulation cycle.
        This drives aging, metabolism, and lifecycle changes.
        """
        self.metabolism.age += 1
        self.metabolism.nectar_level -= 1  # Base metabolic cost
        self._update_lifecycle_state()
        self._update_affective_state()

    @abstractmethod
    def main_function(self, *args, **kwargs):
        """
        The core purpose of the bee, to be implemented by subclasses.
        e.g., for an Aggregate, this would be `handle_command`.
        """
        pass

    def _update_lifecycle_state(self):
        """The state machine logic for the bee's life."""
        if (
            self.metabolism.nectar_level <= 10
            and self.lifecycle_state == LifecycleState.ACTIVE
        ):
            self.lifecycle_state = LifecycleState.HIBERNATING
        elif (
            self.metabolism.nectar_level > 10
            and self.lifecycle_state == LifecycleState.HIBERNATING
        ):
            self.lifecycle_state = LifecycleState.ACTIVE

    def _update_affective_state(self):
        """Update emotions based on health and experiences."""
        if self.metabolism.health_status == HealthStatus.STARVING:
            self.metabolism.affective_state["pain"] += 1
        elif self.metabolism.health_status == HealthStatus.TOXIC:
            self.metabolism.affective_state["fear"] += 1

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} id={self.id} "
            f"symbol={self.symbol.name} "
            f"state={self.lifecycle_state.name} "
            f"nectar={self.metabolism.nectar_level} "
            f"age={self.metabolism.age}>"
        )
