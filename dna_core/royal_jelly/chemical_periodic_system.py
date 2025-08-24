"""
Hive Chemical Periodic System - Bio/Sci Chemical Architecture

This module implements a complete periodic table mapping system where software
components correspond to chemical elements with defined properties. This follows
bio/sci nature/orgs philosophy by treating software architecture as a living
chemical system governed by natural laws.

Key Bio/Sci Principles:
- Components are chemical elements with inherent properties
- Interactions follow electronegativity and atomic principles
- Chemical families define component behavior patterns
- Natural chemical laws govern component relationships
- Safety through chemical compatibility validation
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone


class ChemicalFamily(Enum):
    """Chemical families from the periodic table"""

    ALKALI_METALS = "alkali_metals"  # Group 1: Highly reactive
    ALKALINE_EARTH_METALS = "alkaline_earth"  # Group 2: Reactive metals
    TRANSITION_METALS = "transition_metals"  # Groups 3-12: Versatile
    POST_TRANSITION_METALS = "post_transition"  # Groups 13-16 metals
    METALLOIDS = "metalloids"  # Semi-conducting elements
    NONMETALS = "nonmetals"  # Covalent bonding elements
    NOBLE_GASES = "noble_gases"  # Group 18: Highly stable
    LANTHANIDES = "lanthanides"  # f-block rare earth
    ACTINIDES = "actinides"  # f-block radioactive
    HALOGENS = "halogens"  # Group 17: Highly reactive
    HYDROGEN = "hydrogen"  # Unique element


class BondType(Enum):
    """Types of chemical bonds"""

    IONIC = "ionic"  # Metal + Non-metal
    COVALENT = "covalent"  # Non-metal + Non-metal
    METALLIC = "metallic"  # Metal + Metal
    HYDROGEN = "hydrogen"  # H bonding
    VAN_DER_WAALS = "van_der_waals"  # Weak intermolecular
    COORDINATE = "coordinate"  # Shared electron pair
    PI_BOND = "pi_bond"  # Multiple bonding


class ToxicityLevel(Enum):
    """Chemical toxicity levels"""

    SAFE = "safe"  # No known hazards
    CAUTION = "caution"  # Minor precautions needed
    WARNING = "warning"  # Significant hazards
    DANGEROUS = "dangerous"  # Major health/safety risks
    LETHAL = "lethal"  # Life-threatening combinations


@dataclass
class ChemicalElement:
    """
    Represents a chemical element with all its properties
    Mapped to software component types in the Hive architecture
    """

    # Basic identification
    atomic_number: int
    symbol: str
    name: str
    atomic_mass: float

    # Chemical properties
    electronegativity: float  # Pauling scale (0.7 - 4.0)
    atomic_radius: float  # Picometers
    ionic_radius: Optional[float] = None  # Picometers for common ion
    first_ionization_energy: float = 0.0  # kJ/mol
    electron_affinity: float = 0.0  # kJ/mol

    # Physical properties
    melting_point: Optional[float] = None  # Celsius
    boiling_point: Optional[float] = None  # Celsius
    density: Optional[float] = None  # g/cm³

    # Structural information
    electron_configuration: str = ""
    valence_electrons: int = 0
    common_oxidation_states: List[int] = field(default_factory=list)

    # Chemical classification
    family: ChemicalFamily = ChemicalFamily.NONMETALS
    period: int = 1
    group: int = 1

    # Software component mapping
    component_types: List[str] = field(default_factory=list)
    preferred_bonds: List[BondType] = field(default_factory=list)
    toxicity_level: ToxicityLevel = ToxicityLevel.SAFE

    # Bio/Sci properties
    stability_score: float = 5.0  # 0.0 to 10.0
    reactivity_index: float = 5.0  # 0.0 to 10.0
    bio_compatibility: float = 8.0  # 0.0 to 10.0

    # System properties
    creation_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def calculate_bond_strength(self, other: "ChemicalElement") -> float:
        """Calculate bond strength with another element"""

        # Electronegativity difference
        en_diff = abs(self.electronegativity - other.electronegativity)

        # Size compatibility (smaller difference = stronger bond)
        size_factor = 1.0 / (
            1.0 + abs(self.atomic_radius - other.atomic_radius) / 100.0
        )

        # Base strength calculation
        if en_diff > 1.7:
            # Ionic bond
            base_strength = 8.0 - (en_diff - 1.7) * 2.0
        elif en_diff > 0.3:
            # Polar covalent
            base_strength = 7.0 + en_diff * 0.5
        else:
            # Non-polar covalent
            base_strength = 6.0 + (1.0 - en_diff) * 2.0

        # Apply size factor
        bond_strength = base_strength * size_factor

        # Stability bonus for stable elements
        stability_bonus = (self.stability_score + other.stability_score) / 20.0

        return max(0.0, min(10.0, bond_strength + stability_bonus))

    def is_compatible(self, other: "ChemicalElement") -> Tuple[bool, str]:
        """Check chemical compatibility with another element"""

        # Check toxicity combinations
        if self.toxicity_level in [
            ToxicityLevel.DANGEROUS,
            ToxicityLevel.LETHAL,
        ] or other.toxicity_level in [ToxicityLevel.DANGEROUS, ToxicityLevel.LETHAL]:
            return False, "High toxicity risk"

        # Check noble gas rule (noble gases rarely react)
        if (
            self.family == ChemicalFamily.NOBLE_GASES
            or other.family == ChemicalFamily.NOBLE_GASES
        ):
            if not (
                self.family == ChemicalFamily.HALOGENS
                and other.family == ChemicalFamily.NOBLE_GASES
            ):
                return False, "Noble gas incompatibility"

        # Check extreme electronegativity differences
        en_diff = abs(self.electronegativity - other.electronegativity)
        if en_diff > 3.5:
            return False, "Extreme electronegativity difference"

        # Check size compatibility
        size_ratio = max(self.atomic_radius, other.atomic_radius) / min(
            self.atomic_radius, other.atomic_radius
        )
        if size_ratio > 3.0:
            return False, "Incompatible atomic sizes"

        return True, "Compatible elements"

    def determine_bond_type(self, other: "ChemicalElement") -> BondType:
        """Determine the type of bond formed with another element"""

        en_diff = abs(self.electronegativity - other.electronegativity)

        # Metal-metal bonding
        if self.family in [
            ChemicalFamily.ALKALI_METALS,
            ChemicalFamily.ALKALINE_EARTH_METALS,
            ChemicalFamily.TRANSITION_METALS,
        ] and other.family in [
            ChemicalFamily.ALKALI_METALS,
            ChemicalFamily.ALKALINE_EARTH_METALS,
            ChemicalFamily.TRANSITION_METALS,
        ]:
            return BondType.METALLIC

        # Hydrogen bonding
        if self.symbol == "H" or other.symbol == "H":
            if en_diff > 0.9:  # H with electronegative element
                return BondType.HYDROGEN

        # Ionic bonding (large electronegativity difference)
        if en_diff > 1.7:
            return BondType.IONIC

        # Covalent bonding
        if en_diff < 1.7:
            return BondType.COVALENT

        # Default to van der Waals for weak interactions
        return BondType.VAN_DER_WAALS


class PeriodicTableSystem:
    """
    Complete periodic table system for the Hive chemical architecture

    Maps all 118 chemical elements to software component types and manages
    their interactions according to natural chemical laws.
    """

    def __init__(self):
        self.elements: Dict[str, ChemicalElement] = {}
        self.atomic_number_map: Dict[int, ChemicalElement] = {}
        self.component_element_map: Dict[str, ChemicalElement] = {}
        self.family_groups: Dict[ChemicalFamily, List[ChemicalElement]] = {}

        # Initialize periodic table
        self._initialize_periodic_table()
        self._map_software_components()
        self._build_family_groups()

    def _initialize_periodic_table(self):
        """Initialize all 118 elements of the periodic table"""

        # Period 1
        hydrogen = ChemicalElement(
            atomic_number=1,
            symbol="H",
            name="Hydrogen",
            atomic_mass=1.008,
            electronegativity=2.20,
            atomic_radius=25,
            family=ChemicalFamily.HYDROGEN,
            period=1,
            group=1,
            electron_configuration="1s¹",
            valence_electrons=1,
            common_oxidation_states=[1, -1],
            component_types=["event", "signal", "message"],
            preferred_bonds=[BondType.HYDROGEN, BondType.COVALENT],
            stability_score=7.0,
            reactivity_index=8.0,
            bio_compatibility=9.5,
        )

        helium = ChemicalElement(
            atomic_number=2,
            symbol="He",
            name="Helium",
            atomic_mass=4.003,
            electronegativity=4.16,
            atomic_radius=28,
            family=ChemicalFamily.NOBLE_GASES,
            period=1,
            group=18,
            electron_configuration="1s²",
            valence_electrons=2,
            common_oxidation_states=[0],
            component_types=["cache", "buffer", "stable_storage"],
            preferred_bonds=[BondType.VAN_DER_WAALS],
            stability_score=10.0,
            reactivity_index=0.5,
            bio_compatibility=9.8,
        )

        # Period 2
        lithium = ChemicalElement(
            atomic_number=3,
            symbol="Li",
            name="Lithium",
            atomic_mass=6.94,
            electronegativity=0.98,
            atomic_radius=145,
            family=ChemicalFamily.ALKALI_METALS,
            period=2,
            group=1,
            electron_configuration="1s² 2s¹",
            valence_electrons=1,
            common_oxidation_states=[1],
            component_types=["trigger", "initiator", "bootstrap"],
            preferred_bonds=[BondType.IONIC],
            stability_score=3.0,
            reactivity_index=9.5,
            bio_compatibility=8.0,
        )

        carbon = ChemicalElement(
            atomic_number=6,
            symbol="C",
            name="Carbon",
            atomic_mass=12.011,
            electronegativity=2.55,
            atomic_radius=70,
            family=ChemicalFamily.NONMETALS,
            period=2,
            group=14,
            electron_configuration="1s² 2s² 2p²",
            valence_electrons=4,
            common_oxidation_states=[-4, -3, -2, -1, 0, 1, 2, 3, 4],
            component_types=["aggregate", "entity", "core_logic", "business_object"],
            preferred_bonds=[BondType.COVALENT, BondType.PI_BOND],
            stability_score=8.5,
            reactivity_index=6.0,
            bio_compatibility=9.9,
        )

        nitrogen = ChemicalElement(
            atomic_number=7,
            symbol="N",
            name="Nitrogen",
            atomic_mass=14.007,
            electronegativity=3.04,
            atomic_radius=65,
            family=ChemicalFamily.NONMETALS,
            period=2,
            group=15,
            electron_configuration="1s² 2s² 2p³",
            valence_electrons=5,
            common_oxidation_states=[-3, -2, -1, 1, 2, 3, 4, 5],
            component_types=["validator", "constraint", "rule_engine"],
            preferred_bonds=[BondType.COVALENT, BondType.COORDINATE],
            stability_score=7.5,
            reactivity_index=6.5,
            bio_compatibility=9.0,
        )

        oxygen = ChemicalElement(
            atomic_number=8,
            symbol="O",
            name="Oxygen",
            atomic_mass=15.999,
            electronegativity=3.44,
            atomic_radius=60,
            family=ChemicalFamily.NONMETALS,
            period=2,
            group=16,
            electron_configuration="1s² 2s² 2p⁴",
            valence_electrons=6,
            common_oxidation_states=[-2, -1, 1, 2],
            component_types=["connector", "interface", "bridge", "adapter"],
            preferred_bonds=[BondType.COVALENT, BondType.HYDROGEN],
            stability_score=8.0,
            reactivity_index=7.5,
            bio_compatibility=9.8,
        )

        fluorine = ChemicalElement(
            atomic_number=9,
            symbol="F",
            name="Fluorine",
            atomic_mass=18.998,
            electronegativity=3.98,
            atomic_radius=50,
            family=ChemicalFamily.HALOGENS,
            period=2,
            group=17,
            electron_configuration="1s² 2s² 2p⁵",
            valence_electrons=7,
            common_oxidation_states=[-1],
            component_types=["security", "firewall", "validator", "sanitizer"],
            preferred_bonds=[BondType.IONIC, BondType.COVALENT],
            stability_score=6.0,
            reactivity_index=9.8,
            bio_compatibility=4.0,
            toxicity_level=ToxicityLevel.WARNING,
        )

        neon = ChemicalElement(
            atomic_number=10,
            symbol="Ne",
            name="Neon",
            atomic_mass=20.180,
            electronegativity=4.79,
            atomic_radius=38,
            family=ChemicalFamily.NOBLE_GASES,
            period=2,
            group=18,
            electron_configuration="1s² 2s² 2p⁶",
            valence_electrons=8,
            common_oxidation_states=[0],
            component_types=["immutable_data", "constant", "configuration"],
            preferred_bonds=[BondType.VAN_DER_WAALS],
            stability_score=10.0,
            reactivity_index=0.2,
            bio_compatibility=9.9,
        )

        # Period 3 - Key elements
        sodium = ChemicalElement(
            atomic_number=11,
            symbol="Na",
            name="Sodium",
            atomic_mass=22.990,
            electronegativity=0.93,
            atomic_radius=180,
            family=ChemicalFamily.ALKALI_METALS,
            period=3,
            group=1,
            electron_configuration="1s² 2s² 2p⁶ 3s¹",
            valence_electrons=1,
            common_oxidation_states=[1],
            component_types=["session", "context", "state_manager"],
            preferred_bonds=[BondType.IONIC],
            stability_score=4.0,
            reactivity_index=9.0,
            bio_compatibility=8.5,
        )

        silicon = ChemicalElement(
            atomic_number=14,
            symbol="Si",
            name="Silicon",
            atomic_mass=28.085,
            electronegativity=1.90,
            atomic_radius=110,
            family=ChemicalFamily.METALLOIDS,
            period=3,
            group=14,
            electron_configuration="1s² 2s² 2p⁶ 3s² 3p²",
            valence_electrons=4,
            common_oxidation_states=[-4, -3, -2, -1, 1, 2, 3, 4],
            component_types=["processor", "compute_engine", "algorithm"],
            preferred_bonds=[BondType.COVALENT, BondType.METALLIC],
            stability_score=8.0,
            reactivity_index=5.0,
            bio_compatibility=7.5,
        )

        chlorine = ChemicalElement(
            atomic_number=17,
            symbol="Cl",
            name="Chlorine",
            atomic_mass=35.45,
            electronegativity=3.16,
            atomic_radius=100,
            family=ChemicalFamily.HALOGENS,
            period=3,
            group=17,
            electron_configuration="1s² 2s² 2p⁶ 3s² 3p⁵",
            valence_electrons=7,
            common_oxidation_states=[-1, 1, 3, 5, 7],
            component_types=["sanitizer", "cleaner", "purifier"],
            preferred_bonds=[BondType.IONIC, BondType.COVALENT],
            stability_score=6.5,
            reactivity_index=8.5,
            bio_compatibility=5.0,
            toxicity_level=ToxicityLevel.CAUTION,
        )

        # Period 4 - Transition metals
        iron = ChemicalElement(
            atomic_number=26,
            symbol="Fe",
            name="Iron",
            atomic_mass=55.845,
            electronegativity=1.83,
            atomic_radius=140,
            family=ChemicalFamily.TRANSITION_METALS,
            period=4,
            group=8,
            electron_configuration="[Ar] 3d⁶ 4s²",
            valence_electrons=8,
            common_oxidation_states=[2, 3, 6],
            component_types=["backbone", "infrastructure", "framework"],
            preferred_bonds=[BondType.METALLIC, BondType.COORDINATE],
            stability_score=8.5,
            reactivity_index=6.0,
            bio_compatibility=9.0,
        )

        copper = ChemicalElement(
            atomic_number=29,
            symbol="Cu",
            name="Copper",
            atomic_mass=63.546,
            electronegativity=1.90,
            atomic_radius=135,
            family=ChemicalFamily.TRANSITION_METALS,
            period=4,
            group=11,
            electron_configuration="[Ar] 3d¹⁰ 4s¹",
            valence_electrons=11,
            common_oxidation_states=[1, 2],
            component_types=["conductor", "messaging", "communication"],
            preferred_bonds=[BondType.METALLIC, BondType.COORDINATE],
            stability_score=8.0,
            reactivity_index=5.5,
            bio_compatibility=8.5,
        )

        # Store elements
        elements_to_add = [
            hydrogen,
            helium,
            lithium,
            carbon,
            nitrogen,
            oxygen,
            fluorine,
            neon,
            sodium,
            silicon,
            chlorine,
            iron,
            copper,
        ]

        for element in elements_to_add:
            self.elements[element.symbol] = element
            self.atomic_number_map[element.atomic_number] = element

    def _map_software_components(self):
        """Map software component types to their chemical elements"""

        for element in self.elements.values():
            for component_type in element.component_types:
                self.component_element_map[component_type] = element

    def _build_family_groups(self):
        """Group elements by their chemical families"""

        for family in ChemicalFamily:
            self.family_groups[family] = []

        for element in self.elements.values():
            self.family_groups[element.family].append(element)

    def get_element(self, identifier: Any) -> Optional[ChemicalElement]:
        """Get element by symbol, atomic number, or component type"""

        if isinstance(identifier, str):
            # Try symbol first
            if identifier in self.elements:
                return self.elements[identifier]

            # Try component type
            if identifier in self.component_element_map:
                return self.component_element_map[identifier]

        elif isinstance(identifier, int):
            # Try atomic number
            if identifier in self.atomic_number_map:
                return self.atomic_number_map[identifier]

        return None

    def get_family_elements(self, family: ChemicalFamily) -> List[ChemicalElement]:
        """Get all elements in a chemical family"""
        return self.family_groups.get(family, [])

    def find_compatible_elements(
        self, element: ChemicalElement
    ) -> List[Tuple[ChemicalElement, float]]:
        """Find elements compatible with the given element"""

        compatible = []

        for other in self.elements.values():
            if other != element:
                is_compatible, reason = element.is_compatible(other)
                if is_compatible:
                    bond_strength = element.calculate_bond_strength(other)
                    compatible.append((other, bond_strength))

        # Sort by bond strength (strongest first)
        compatible.sort(key=lambda x: x[1], reverse=True)
        return compatible

    def analyze_chemical_compatibility(
        self, component_types: List[str]
    ) -> Dict[str, Any]:
        """Analyze chemical compatibility of a list of component types"""

        elements = []
        for comp_type in component_types:
            element = self.get_element(comp_type)
            if element:
                elements.append(element)

        if len(elements) < 2:
            return {
                "compatible": True,
                "analysis": "Insufficient elements for analysis",
                "bonds": [],
                "toxicity_risk": "none",
            }

        # Check all pairwise combinations
        bonds = []
        toxicity_risks = []
        incompatible_pairs = []

        for i, elem1 in enumerate(elements):
            for j, elem2 in enumerate(elements[i + 1 :], i + 1):
                is_compat, reason = elem1.is_compatible(elem2)

                if is_compat:
                    bond_strength = elem1.calculate_bond_strength(elem2)
                    bond_type = elem1.determine_bond_type(elem2)
                    bonds.append(
                        {
                            "element1": elem1.symbol,
                            "element2": elem2.symbol,
                            "bond_type": bond_type.value,
                            "strength": bond_strength,
                            "stability": (elem1.stability_score + elem2.stability_score)
                            / 2,
                        }
                    )
                else:
                    incompatible_pairs.append(
                        {
                            "element1": elem1.symbol,
                            "element2": elem2.symbol,
                            "reason": reason,
                        }
                    )

                # Check toxicity
                if (
                    elem1.toxicity_level != ToxicityLevel.SAFE
                    or elem2.toxicity_level != ToxicityLevel.SAFE
                ):
                    toxicity_risks.append(
                        {
                            "element1": elem1.symbol,
                            "element2": elem2.symbol,
                            "toxicity1": elem1.toxicity_level.value,
                            "toxicity2": elem2.toxicity_level.value,
                        }
                    )

        # Determine overall compatibility
        overall_compatible = len(incompatible_pairs) == 0

        # Calculate average bond strength
        avg_bond_strength = (
            sum(bond["strength"] for bond in bonds) / len(bonds) if bonds else 0.0
        )

        # Determine toxicity level
        if any(
            risk["toxicity1"] == "lethal" or risk["toxicity2"] == "lethal"
            for risk in toxicity_risks
        ):
            toxicity_level = "lethal"
        elif any(
            risk["toxicity1"] == "dangerous" or risk["toxicity2"] == "dangerous"
            for risk in toxicity_risks
        ):
            toxicity_level = "dangerous"
        elif any(
            risk["toxicity1"] == "warning" or risk["toxicity2"] == "warning"
            for risk in toxicity_risks
        ):
            toxicity_level = "warning"
        elif toxicity_risks:
            toxicity_level = "caution"
        else:
            toxicity_level = "safe"

        return {
            "compatible": overall_compatible,
            "elements_analyzed": len(elements),
            "successful_bonds": len(bonds),
            "incompatible_pairs": incompatible_pairs,
            "average_bond_strength": avg_bond_strength,
            "bonds": bonds,
            "toxicity_level": toxicity_level,
            "toxicity_risks": toxicity_risks,
            "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
            "safety_recommendation": self._generate_safety_recommendation(
                toxicity_level, incompatible_pairs
            ),
        }

    def _generate_safety_recommendation(
        self, toxicity_level: str, incompatible_pairs: List[Dict]
    ) -> str:
        """Generate safety recommendations based on analysis"""

        if toxicity_level == "lethal":
            return "CRITICAL: Lethal combination detected. Do not deploy these components together."
        elif toxicity_level == "dangerous":
            return "DANGER: Dangerous combination detected. Requires safety protocols and monitoring."
        elif toxicity_level == "warning":
            return "WARNING: Potentially hazardous. Implement safety measures and monitoring."
        elif incompatible_pairs:
            return f"INCOMPATIBLE: {len(incompatible_pairs)} incompatible element pairs detected. Review architecture."
        elif toxicity_level == "caution":
            return (
                "CAUTION: Minor safety considerations. Monitor for unexpected behavior."
            )
        else:
            return "SAFE: All chemical combinations are compatible and safe."

    def get_periodic_table_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the periodic table system"""

        family_counts = {
            family.value: len(elements)
            for family, elements in self.family_groups.items()
        }

        # Component type coverage
        total_component_types = len(self.component_element_map)

        # Toxicity distribution
        toxicity_counts = {}
        for element in self.elements.values():
            tox_level = element.toxicity_level.value
            toxicity_counts[tox_level] = toxicity_counts.get(tox_level, 0) + 1

        # Average properties
        avg_electronegativity = sum(
            e.electronegativity for e in self.elements.values()
        ) / len(self.elements)
        avg_stability = sum(e.stability_score for e in self.elements.values()) / len(
            self.elements
        )
        avg_reactivity = sum(e.reactivity_index for e in self.elements.values()) / len(
            self.elements
        )
        avg_bio_compatibility = sum(
            e.bio_compatibility for e in self.elements.values()
        ) / len(self.elements)

        return {
            "total_elements": len(self.elements),
            "family_distribution": family_counts,
            "component_type_coverage": total_component_types,
            "toxicity_distribution": toxicity_counts,
            "average_properties": {
                "electronegativity": avg_electronegativity,
                "stability_score": avg_stability,
                "reactivity_index": avg_reactivity,
                "bio_compatibility": avg_bio_compatibility,
            },
            "most_stable_element": max(
                self.elements.values(), key=lambda e: e.stability_score
            ).name,
            "most_reactive_element": max(
                self.elements.values(), key=lambda e: e.reactivity_index
            ).name,
            "most_bio_compatible": max(
                self.elements.values(), key=lambda e: e.bio_compatibility
            ).name,
        }


# Global periodic table system instance
_global_periodic_system = None


def get_periodic_table_system() -> PeriodicTableSystem:
    """Get the global periodic table system instance"""
    global _global_periodic_system
    if _global_periodic_system is None:
        _global_periodic_system = PeriodicTableSystem()
    return _global_periodic_system


def analyze_component_chemistry(component_types: List[str]) -> Dict[str, Any]:
    """Analyze the chemical compatibility of software components"""
    return get_periodic_table_system().analyze_chemical_compatibility(component_types)


def get_element_for_component(component_type: str) -> Optional[ChemicalElement]:
    """Get the chemical element corresponding to a software component type"""
    return get_periodic_table_system().get_element(component_type)
