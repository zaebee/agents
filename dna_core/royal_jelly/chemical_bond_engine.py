"""
Hive Chemical Bond Management Engine - Bio/Sci Bond Architecture

This module implements a comprehensive chemical bond management system that
governs interactions between software components based on chemical principles.
Bonds form, strengthen, weaken, and break according to natural chemical laws.

Key Bio/Sci Principles:
- Bonds form based on electronegativity and atomic compatibility
- Bond strength varies with chemical environment and stress
- Bond breaking and formation follow thermodynamic principles
- Chemical equilibrium maintains system stability
- Catalysts can accelerate bond formation/breaking without being consumed
"""

from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid
import math
import random
from datetime import datetime, timezone
from collections import defaultdict, deque
import threading

from .chemical_periodic_system import (
    ChemicalElement,
    BondType,
    get_periodic_table_system,
)


class BondState(Enum):
    """States of chemical bonds"""

    FORMING = "forming"  # Bond in process of formation
    STABLE = "stable"  # Fully formed, stable bond
    STRAINED = "strained"  # Under stress, weakened
    BREAKING = "breaking"  # Bond in process of breaking
    BROKEN = "broken"  # Bond has been severed
    CATALYZED = "catalyzed"  # Bond formation assisted by catalyst


class ReactionType(Enum):
    """Types of chemical reactions"""

    SYNTHESIS = "synthesis"  # A + B → AB
    DECOMPOSITION = "decomposition"  # AB → A + B
    SINGLE_REPLACEMENT = "single_replacement"  # A + BC → AC + B
    DOUBLE_REPLACEMENT = "double_replacement"  # AB + CD → AD + CB
    COMBUSTION = "combustion"  # Fuel + O₂ → CO₂ + H₂O
    REDOX = "redox"  # Electron transfer reactions
    ACID_BASE = "acid_base"  # Proton transfer reactions
    CATALYTIC = "catalytic"  # Catalyst-assisted reactions


@dataclass
class ChemicalBond:
    """Represents a chemical bond between two components"""

    bond_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # Bond participants
    element1: ChemicalElement = None
    element2: ChemicalElement = None
    component1_id: str = ""
    component2_id: str = ""

    # Bond properties
    bond_type: BondType = BondType.COVALENT
    bond_strength: float = 5.0  # 0.0 to 10.0
    bond_length: float = 150.0  # Picometers
    bond_energy: float = 400.0  # kJ/mol

    # Bond state and dynamics
    state: BondState = BondState.FORMING
    formation_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_stress_test: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    stress_level: float = 0.0  # 0.0 to 1.0

    # Environmental factors
    temperature: float = 298.15  # Kelvin (25°C default)
    pressure: float = 1.0  # Atmospheres
    ph_level: float = 7.0  # pH scale
    ionic_strength: float = 0.0  # Molarity

    # Performance metrics
    stability_score: float = 8.0  # 0.0 to 10.0
    formation_energy: float = -200.0  # kJ/mol (negative = favorable)
    activation_count: int = 0
    failure_count: int = 0

    # Bio/Sci properties
    biological_compatibility: float = 8.0
    evolutionary_fitness: float = 7.0
    adaptive_capacity: float = 6.0

    # Catalysis
    catalyst_element: Optional[ChemicalElement] = None
    catalytic_efficiency: float = 1.0

    def calculate_bond_stability(self) -> float:
        """Calculate current bond stability based on all factors"""

        # Base stability from bond strength
        base_stability = self.bond_strength / 10.0

        # Temperature effects (higher temp = less stable for most bonds)
        temp_factor = 1.0 - (self.temperature - 298.15) / 1000.0
        temp_factor = max(0.1, min(1.0, temp_factor))

        # Pressure effects (usually minimal for covalent bonds)
        pressure_factor = 1.0 + (self.pressure - 1.0) * 0.1
        pressure_factor = max(0.5, min(1.5, pressure_factor))

        # pH effects
        optimal_ph = 7.0
        ph_deviation = abs(self.ph_level - optimal_ph)
        ph_factor = max(0.3, 1.0 - ph_deviation / 14.0)

        # Stress effects
        stress_factor = max(0.1, 1.0 - self.stress_level)

        # Calculate combined stability
        combined_stability = (
            base_stability * temp_factor * pressure_factor * ph_factor * stress_factor
        )

        return max(0.0, min(10.0, combined_stability * 10.0))

    def apply_stress(
        self, stress_amount: float, stress_type: str = "mechanical"
    ) -> bool:
        """Apply stress to the bond and check if it breaks"""

        self.stress_level = min(1.0, self.stress_level + stress_amount)
        self.last_stress_test = datetime.now(timezone.utc)

        current_stability = self.calculate_bond_stability()

        # Check if bond breaks under stress
        break_threshold = 2.0 + random.uniform(-0.5, 0.5)

        if current_stability < break_threshold:
            self.state = BondState.BREAKING
            self.failure_count += 1
            return False  # Bond broken
        elif current_stability < 4.0:
            self.state = BondState.STRAINED
        else:
            self.state = BondState.STABLE

        return True  # Bond survived

    def heal_bond(self, healing_factor: float = 0.1):
        """Allow bond to heal and recover from stress"""

        self.stress_level = max(0.0, self.stress_level - healing_factor)

        if self.stress_level < 0.1:
            self.state = BondState.STABLE
        elif self.stress_level < 0.5:
            self.state = BondState.STRAINED

    def catalyze_bond(self, catalyst: ChemicalElement, efficiency: float = 2.0):
        """Apply catalytic effects to bond formation/strength"""

        self.catalyst_element = catalyst
        self.catalytic_efficiency = efficiency
        self.state = BondState.CATALYZED

        # Catalysts lower activation energy and increase reaction rate
        self.formation_energy *= 1.0 / efficiency
        self.bond_strength = min(10.0, self.bond_strength * 1.2)

    def get_bond_health_metrics(self) -> Dict[str, Any]:
        """Get comprehensive bond health metrics"""

        return {
            "bond_id": self.bond_id,
            "state": self.state.value,
            "stability_score": self.calculate_bond_stability(),
            "stress_level": self.stress_level,
            "bond_strength": self.bond_strength,
            "activation_count": self.activation_count,
            "failure_count": self.failure_count,
            "success_rate": (self.activation_count - self.failure_count)
            / max(1, self.activation_count),
            "age_seconds": (
                datetime.now(timezone.utc) - self.formation_time
            ).total_seconds(),
            "environmental_conditions": {
                "temperature": self.temperature,
                "pressure": self.pressure,
                "ph_level": self.ph_level,
                "ionic_strength": self.ionic_strength,
            },
            "catalyzed": self.catalyst_element is not None,
            "catalytic_efficiency": self.catalytic_efficiency
            if self.catalyst_element
            else None,
        }


@dataclass
class ChemicalReaction:
    """Represents a chemical reaction between components"""

    reaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reaction_type: ReactionType = ReactionType.SYNTHESIS

    # Reactants and products
    reactants: List[ChemicalElement] = field(default_factory=list)
    products: List[ChemicalElement] = field(default_factory=list)
    catalyst: Optional[ChemicalElement] = None

    # Reaction properties
    activation_energy: float = 100.0  # kJ/mol
    enthalpy_change: float = -50.0  # kJ/mol (negative = exothermic)
    entropy_change: float = 10.0  # J/(mol·K)
    reaction_rate: float = 1.0  # relative rate

    # Equilibrium
    equilibrium_constant: float = 1.0
    forward_rate_constant: float = 1.0
    reverse_rate_constant: float = 1.0

    # State
    reaction_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completion_percentage: float = 0.0
    is_reversible: bool = True
    is_spontaneous: bool = True

    def calculate_gibbs_free_energy(self, temperature: float = 298.15) -> float:
        """Calculate Gibbs free energy change (ΔG = ΔH - TΔS)"""

        delta_g = self.enthalpy_change - temperature * (self.entropy_change / 1000.0)
        return delta_g

    def is_thermodynamically_favorable(self, temperature: float = 298.15) -> bool:
        """Check if reaction is thermodynamically favorable (ΔG < 0)"""

        return self.calculate_gibbs_free_energy(temperature) < 0

    def calculate_reaction_rate(
        self, concentrations: List[float], temperature: float = 298.15
    ) -> float:
        """Calculate reaction rate using Arrhenius equation"""

        # Arrhenius equation: k = A * e^(-Ea/RT)
        R = 8.314  # Gas constant J/(mol·K)

        # Catalytic effect
        effective_activation_energy = self.activation_energy
        if self.catalyst:
            effective_activation_energy *= 0.5  # Catalyst reduces activation energy

        # Rate constant
        rate_constant = self.forward_rate_constant * math.exp(
            -effective_activation_energy * 1000 / (R * temperature)
        )

        # Rate depends on concentrations (simplified first-order kinetics)
        concentration_factor = 1.0
        for conc in concentrations:
            concentration_factor *= conc

        return rate_constant * concentration_factor

    def update_completion(self, time_step: float = 1.0, temperature: float = 298.15):
        """Update reaction completion based on kinetics"""

        if self.completion_percentage >= 100.0:
            return

        # Simple first-order kinetics simulation
        rate = self.calculate_reaction_rate([1.0] * len(self.reactants), temperature)

        # Update completion
        delta_completion = rate * time_step / 10.0  # Scale factor
        self.completion_percentage = min(
            100.0, self.completion_percentage + delta_completion
        )


class ChemicalBondEngine:
    """
    Chemical Bond Management Engine for the Hive Architecture

    Manages formation, maintenance, and breaking of chemical bonds between
    software components according to natural chemical principles.
    """

    def __init__(self):
        self.periodic_system = get_periodic_table_system()

        # Bond management
        self.active_bonds: Dict[str, ChemicalBond] = {}
        self.bond_history: deque = deque(maxlen=1000)
        self.component_bonds: Dict[str, Set[str]] = defaultdict(set)

        # Reaction management
        self.active_reactions: Dict[str, ChemicalReaction] = {}
        self.reaction_history: deque = deque(maxlen=500)

        # Environmental conditions
        self.global_temperature: float = 298.15  # Kelvin
        self.global_pressure: float = 1.0  # Atmospheres
        self.global_ph: float = 7.0  # pH scale

        # Catalysts
        self.available_catalysts: Dict[str, ChemicalElement] = {}
        self.catalyst_usage: Dict[str, int] = defaultdict(int)

        # Performance tracking
        self.bond_formation_count: int = 0
        self.bond_breaking_count: int = 0
        self.successful_reactions: int = 0
        self.failed_reactions: int = 0

        # Thread safety
        self._lock = threading.RLock()

        # Initialize catalysts
        self._initialize_catalysts()

    def _initialize_catalysts(self):
        """Initialize common catalysts for chemical reactions"""

        # Platinum - excellent catalyst for many reactions
        if "Pt" in self.periodic_system.elements:
            self.available_catalysts["platinum"] = self.periodic_system.elements["Pt"]

        # Iron - common catalyst for industrial processes
        if "Fe" in self.periodic_system.elements:
            self.available_catalysts["iron"] = self.periodic_system.elements["Fe"]

        # Copper - good conductor and catalyst
        if "Cu" in self.periodic_system.elements:
            self.available_catalysts["copper"] = self.periodic_system.elements["Cu"]

    def form_chemical_bond(
        self,
        component1_id: str,
        component1_type: str,
        component2_id: str,
        component2_type: str,
        catalyst_name: Optional[str] = None,
    ) -> Optional[ChemicalBond]:
        """Form a chemical bond between two components"""

        with self._lock:
            # Get chemical elements for components
            element1 = self.periodic_system.get_element(component1_type)
            element2 = self.periodic_system.get_element(component2_type)

            if not element1 or not element2:
                return None

            # Check compatibility
            is_compatible, reason = element1.is_compatible(element2)
            if not is_compatible:
                return None

            # Calculate bond properties
            bond_strength = element1.calculate_bond_strength(element2)
            bond_type = element1.determine_bond_type(element2)
            bond_length = (element1.atomic_radius + element2.atomic_radius) * 0.8

            # Create bond
            bond = ChemicalBond(
                element1=element1,
                element2=element2,
                component1_id=component1_id,
                component2_id=component2_id,
                bond_type=bond_type,
                bond_strength=bond_strength,
                bond_length=bond_length,
                temperature=self.global_temperature,
                pressure=self.global_pressure,
                ph_level=self.global_ph,
            )

            # Apply catalyst if specified
            if catalyst_name and catalyst_name in self.available_catalysts:
                catalyst = self.available_catalysts[catalyst_name]
                bond.catalyze_bond(catalyst, efficiency=1.5)
                self.catalyst_usage[catalyst_name] += 1

            # Calculate formation energy
            bond.formation_energy = -bond_strength * 50.0  # Approximate correlation

            # Store bond
            self.active_bonds[bond.bond_id] = bond
            self.component_bonds[component1_id].add(bond.bond_id)
            self.component_bonds[component2_id].add(bond.bond_id)

            # Update metrics
            self.bond_formation_count += 1

            # Set stable state
            bond.state = BondState.STABLE

            return bond

    def break_chemical_bond(self, bond_id: str, force: bool = False) -> bool:
        """Break a chemical bond"""

        with self._lock:
            if bond_id not in self.active_bonds:
                return False

            bond = self.active_bonds[bond_id]

            if not force:
                # Check if bond can be broken under current conditions
                stability = bond.calculate_bond_stability()
                if stability > 5.0:  # Strong bond, hard to break
                    return False

            # Break the bond
            bond.state = BondState.BROKEN

            # Remove from active bonds
            del self.active_bonds[bond_id]

            # Remove from component mappings
            self.component_bonds[bond.component1_id].discard(bond_id)
            self.component_bonds[bond.component2_id].discard(bond_id)

            # Store in history
            self.bond_history.append(bond)

            # Update metrics
            self.bond_breaking_count += 1

            return True

    def strengthen_bond(self, bond_id: str, strengthening_factor: float = 1.2) -> bool:
        """Strengthen an existing chemical bond"""

        with self._lock:
            if bond_id not in self.active_bonds:
                return False

            bond = self.active_bonds[bond_id]

            # Strengthen the bond
            bond.bond_strength = min(10.0, bond.bond_strength * strengthening_factor)
            bond.stability_score = min(
                10.0, bond.stability_score * strengthening_factor
            )

            # Heal any stress
            bond.heal_bond(0.5)

            return True

    def apply_stress_to_bond(
        self, bond_id: str, stress_amount: float, stress_type: str = "mechanical"
    ) -> bool:
        """Apply stress to a chemical bond"""

        with self._lock:
            if bond_id not in self.active_bonds:
                return False

            bond = self.active_bonds[bond_id]
            bond_survived = bond.apply_stress(stress_amount, stress_type)

            if not bond_survived:
                # Bond broke under stress
                self.break_chemical_bond(bond_id, force=True)

            return bond_survived

    def create_chemical_reaction(
        self,
        reactant_component_ids: List[str],
        reaction_type: ReactionType = ReactionType.SYNTHESIS,
        catalyst_name: Optional[str] = None,
    ) -> Optional[ChemicalReaction]:
        """Create a chemical reaction between components"""

        with self._lock:
            # Get elements for reactants (this is a simplified approach)
            reactants = []
            for comp_id in reactant_component_ids:
                # In a real system, you'd need to map component IDs to types
                # For now, we'll use a placeholder approach
                pass

            # Create reaction
            reaction = ChemicalReaction(
                reaction_type=reaction_type,
                reactants=reactants,
                activation_energy=random.uniform(50.0, 200.0),
                enthalpy_change=random.uniform(-100.0, 50.0),
                entropy_change=random.uniform(-20.0, 30.0),
            )

            # Apply catalyst if specified
            if catalyst_name and catalyst_name in self.available_catalysts:
                reaction.catalyst = self.available_catalysts[catalyst_name]
                reaction.activation_energy *= 0.6  # Catalyst reduces activation energy
                self.catalyst_usage[catalyst_name] += 1

            # Check if reaction is favorable
            if reaction.is_thermodynamically_favorable(self.global_temperature):
                reaction.is_spontaneous = True
                self.successful_reactions += 1
            else:
                reaction.is_spontaneous = False
                self.failed_reactions += 1

            # Store reaction
            self.active_reactions[reaction.reaction_id] = reaction

            return reaction

    def update_environmental_conditions(
        self,
        temperature: Optional[float] = None,
        pressure: Optional[float] = None,
        ph_level: Optional[float] = None,
    ):
        """Update global environmental conditions"""

        with self._lock:
            if temperature is not None:
                self.global_temperature = max(0.0, temperature)

            if pressure is not None:
                self.global_pressure = max(0.001, pressure)

            if ph_level is not None:
                self.global_ph = max(0.0, min(14.0, ph_level))

            # Update all active bonds with new conditions
            for bond in self.active_bonds.values():
                bond.temperature = self.global_temperature
                bond.pressure = self.global_pressure
                bond.ph_level = self.global_ph

    def get_component_bonds(self, component_id: str) -> List[ChemicalBond]:
        """Get all bonds for a specific component"""

        bonds = []
        bond_ids = self.component_bonds.get(component_id, set())

        for bond_id in bond_ids:
            if bond_id in self.active_bonds:
                bonds.append(self.active_bonds[bond_id])

        return bonds

    def analyze_bond_network(self) -> Dict[str, Any]:
        """Analyze the entire chemical bond network"""

        with self._lock:
            # Basic statistics
            total_bonds = len(self.active_bonds)

            # Bond type distribution
            bond_type_counts = {}
            for bond in self.active_bonds.values():
                bond_type = bond.bond_type.value
                bond_type_counts[bond_type] = bond_type_counts.get(bond_type, 0) + 1

            # Bond state distribution
            bond_state_counts = {}
            for bond in self.active_bonds.values():
                state = bond.state.value
                bond_state_counts[state] = bond_state_counts.get(state, 0) + 1

            # Average properties
            if total_bonds > 0:
                avg_strength = (
                    sum(bond.bond_strength for bond in self.active_bonds.values())
                    / total_bonds
                )
                avg_stability = (
                    sum(
                        bond.calculate_bond_stability()
                        for bond in self.active_bonds.values()
                    )
                    / total_bonds
                )
                avg_stress = (
                    sum(bond.stress_level for bond in self.active_bonds.values())
                    / total_bonds
                )
            else:
                avg_strength = avg_stability = avg_stress = 0.0

            # Network connectivity
            connected_components = len(
                [comp_id for comp_id, bonds in self.component_bonds.items() if bonds]
            )

            # Catalyst usage
            total_catalyzed = sum(
                1 for bond in self.active_bonds.values() if bond.catalyst_element
            )

            return {
                "network_statistics": {
                    "total_active_bonds": total_bonds,
                    "connected_components": connected_components,
                    "bond_formation_rate": self.bond_formation_count,
                    "bond_breaking_rate": self.bond_breaking_count,
                    "network_density": total_bonds
                    / max(1, connected_components * (connected_components - 1) / 2),
                },
                "bond_distribution": {
                    "by_type": bond_type_counts,
                    "by_state": bond_state_counts,
                },
                "average_properties": {
                    "bond_strength": avg_strength,
                    "stability_score": avg_stability,
                    "stress_level": avg_stress,
                },
                "environmental_conditions": {
                    "temperature": self.global_temperature,
                    "pressure": self.global_pressure,
                    "ph_level": self.global_ph,
                },
                "catalysis_statistics": {
                    "catalyzed_bonds": total_catalyzed,
                    "catalyst_usage": dict(self.catalyst_usage),
                    "available_catalysts": list(self.available_catalysts.keys()),
                },
                "reaction_statistics": {
                    "active_reactions": len(self.active_reactions),
                    "successful_reactions": self.successful_reactions,
                    "failed_reactions": self.failed_reactions,
                    "success_rate": self.successful_reactions
                    / max(1, self.successful_reactions + self.failed_reactions),
                },
            }

    def perform_bond_maintenance(self):
        """Perform maintenance on all bonds (healing, cleanup, etc.)"""

        with self._lock:
            bonds_to_remove = []

            for bond_id, bond in self.active_bonds.items():
                # Heal bonds with low stress
                if bond.stress_level < 0.3:
                    bond.heal_bond(0.05)

                # Remove completely broken bonds
                if bond.state == BondState.BROKEN:
                    bonds_to_remove.append(bond_id)

                # Check for spontaneous bond breaking due to instability
                elif bond.calculate_bond_stability() < 1.0:
                    if random.random() < 0.1:  # 10% chance of spontaneous breaking
                        bonds_to_remove.append(bond_id)

            # Remove broken bonds
            for bond_id in bonds_to_remove:
                self.break_chemical_bond(bond_id, force=True)


# Global chemical bond engine instance
_global_bond_engine = None


def get_chemical_bond_engine() -> ChemicalBondEngine:
    """Get the global chemical bond engine instance"""
    global _global_bond_engine
    if _global_bond_engine is None:
        _global_bond_engine = ChemicalBondEngine()
    return _global_bond_engine


def form_component_bond(
    component1_id: str,
    component1_type: str,
    component2_id: str,
    component2_type: str,
    catalyst: Optional[str] = None,
) -> Optional[ChemicalBond]:
    """Form a chemical bond between two components"""
    return get_chemical_bond_engine().form_chemical_bond(
        component1_id, component1_type, component2_id, component2_type, catalyst
    )


def analyze_chemical_network() -> Dict[str, Any]:
    """Analyze the current chemical bond network"""
    return get_chemical_bond_engine().analyze_bond_network()
