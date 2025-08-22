import copy
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
    nectar_production_rate: int = 1


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
    max_nectar: int = 1000
    nectar_production_rate: int = 1  # Passive nectar generation per tick
    health_status: HealthStatus = HealthStatus.HEALTHY
    age: int = 0
    affective_state: Dict[str, int] = field(
        default_factory=lambda: {"pain": 0, "joy": 0, "fear": 0}
    )


class StarvationError(Exception):
    """Raised when an organism cannot perform an action due to lack of nectar."""
    pass


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

    def __init__(self, genome: Genome, generation: int = 1):
        # The Unchanging Soul
        self.genome: Genome = genome
        self.id: str = f"{genome.primitive_type.name}-{uuid.uuid4()}"
        self.generation: int = generation

        # The Learned Memory
        self.epigenome: Epigenome = Epigenome()

        # The Spark of Life
        self.metabolism: Metabolism = Metabolism()
        self.metabolism.nectar_production_rate = genome.nectar_production_rate
        self.fitness_score: float = 0.0

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

        # Passive nectar production and consumption
        base_metabolic_cost = 1
        produced = self.metabolism.nectar_production_rate
        consumed = base_metabolic_cost

        new_nectar_level = self.metabolism.nectar_level + produced - consumed
        self.metabolism.nectar_level = min(new_nectar_level, self.metabolism.max_nectar)

        if self.metabolism.nectar_level <= 0:
            self.metabolism.health_status = HealthStatus.STARVING

        self._update_lifecycle_state()
        self._update_affective_state()

    def consume_nectar(self, amount: int):
        """
        Consumes a given amount of nectar for an action.
        Raises StarvationError if the organism cannot afford it.
        """
        if self.metabolism.nectar_level < amount:
            self.metabolism.health_status = HealthStatus.STARVING
            raise StarvationError(
                f"{self.id} has {self.metabolism.nectar_level} nectar, but needs {amount}."
            )
        self.metabolism.nectar_level -= amount

    def learn_engram(self, key: str, value: Any):
        """Learns and stores a new piece of wisdom in its epigenome."""
        print(f"  -> {self.id} learned a new engram: {key}={value}")
        self.epigenome.engrams[key] = value

    def replicate(self) -> "DigitalOrganism":
        """
        Creates a child organism that inherits its genome and epigenome.
        The parent endows the child with a portion of its nectar as a
        starting inheritance.
        """
        print(f"  -> {self.id} is replicating...")
        child = self.__class__(genome=self.genome, generation=self.generation + 1)
        child.epigenome = copy.deepcopy(self.epigenome)
        child.epigenome.lineage = {"parent_id": self.id, "parent_generation": self.generation}

        # Inheritance Grant: Parent gives 40% of its nectar to the child
        inheritance_amount = int(self.metabolism.nectar_level * 0.4)
        self.consume_nectar(inheritance_amount)
        child.metabolism.nectar_level = inheritance_amount

        print(f"     ...Child {child.id} (Gen {child.generation}) born with {inheritance_amount} nectar inheritance.")
        return child

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
            f"gen={self.generation} "
            f"state={self.lifecycle_state.name} "
            f"nectar={self.metabolism.nectar_level} "
            f"age={self.metabolism.age} "
            f"fitness={self.fitness_score:.2f}>"
        )
