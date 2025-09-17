#!/usr/bin/env python3
"""
The Reaction Engine - Chemical Reactions for Component Generation
Implements the "Queen Bee" system using chemistry principles.

This transformation handles chemical reactions that create new Hive components,
following conservation laws and reaction mechanisms.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum


class ReactionType(Enum):
    """Types of architectural chemical reactions"""

    SYNTHESIS = "synthesis"  # A + T → AT (combining components)
    DECOMPOSITION = "decomposition"  # AT → A + T (breaking down components)
    SUBSTITUTION = "substitution"  # AC + T → AT + C (replacing parts)
    POLYMERIZATION = "polymerization"  # nA → An (creating complex structures)
    CATALYSIS = "catalysis"  # A + B --catalyst--> AB (accelerated reaction)


class SacredCodon(Enum):
    """The 5 Sacred Codons from the Hive Architecture (from PATTERNS.md)"""

    HANDLE_COMMAND = "handle_command"  # C → A → G (to change the world)
    QUERY_DATA = "query_data"  # C → T → C (to see the world)
    REACT_TO_EVENT = "react_to_event"  # G → C → A → G (to listen to the world)
    IMMUNE_RESPONSE = "immune_response"  # G → C → A → C (to heal the world)
    CHOREOGRAPHY = "choreography"  # Complex multi-step workflows (to become)


@dataclass
class ChemicalReaction:
    """A chemical reaction for creating/modifying components"""

    name: str
    reactants: List[str]
    products: List[str]
    catalysts: List[str] = field(default_factory=list)
    reaction_type: ReactionType = ReactionType.SYNTHESIS
    sacred_codon: Optional[SacredCodon] = None  # Maps to Sacred Codon patterns
    activation_energy: float = 50.0  # Energy needed to start reaction
    heat_released: float = 0.0  # Energy released when reaction occurs
    conditions: Dict[str, str] = field(default_factory=dict)

    def __str__(self) -> str:
        reactants_str = " + ".join(self.reactants)
        products_str = " + ".join(self.products)
        catalyst_str = (
            f" --{', '.join(self.catalysts)}--> " if self.catalysts else " → "
        )
        codon_str = f" [{self.sacred_codon.value}]" if self.sacred_codon else ""
        return f"{reactants_str}{catalyst_str}{products_str}{codon_str}"


@dataclass
class ReactionResult:
    """Result of executing a chemical reaction"""

    success: bool
    products_created: List[str]
    energy_consumed: float
    energy_released: float
    byproducts: List[str] = field(default_factory=list)
    reaction_time: float = 1.0
    side_effects: List[str] = field(default_factory=list)


class ReactionEngine:
    """
    Chemical reaction engine for generating Hive components.
    Implements conservation laws and reaction mechanisms.
    """

    def __init__(self):
        self._known_reactions: Dict[str, ChemicalReaction] = {}
        self._reaction_history: List[Tuple[ChemicalReaction, ReactionResult]] = []
        self._available_catalysts = {
            "royal_jelly": {"efficiency": 2.0, "selectivity": 0.9},
            "genesis_template": {"efficiency": 1.5, "selectivity": 0.8},
            "beekeeper_wisdom": {"efficiency": 1.8, "selectivity": 0.95},
        }

        # Initialize standard reactions
        self._initialize_standard_reactions()

    def _initialize_standard_reactions(self):
        """Initialize the standard set of architectural reactions"""

        # Basic aggregate formation
        self.register_reaction(
            ChemicalReaction(
                name="aggregate_synthesis",
                reactants=["A", "T", "T"],
                products=["A1T2"],
                reaction_type=ReactionType.SYNTHESIS,
                activation_energy=30.0,
                heat_released=15.0,
                conditions={"domain_logic": "required"},
            )
        )

        # Hexagonal architecture formation (like benzene)
        self.register_reaction(
            ChemicalReaction(
                name="hexagonal_formation",
                reactants=["A", "C", "C", "C", "C", "C", "C"],
                products=["HexCore(A1C6)"],
                catalysts=["royal_jelly"],
                reaction_type=ReactionType.POLYMERIZATION,
                activation_energy=80.0,
                heat_released=120.0,
                conditions={"architecture": "hexagonal", "stability": "aromatic"},
            )
        )

        # Event-driven communication
        self.register_reaction(
            ChemicalReaction(
                name="event_generation",
                reactants=["A1T1", "C1"],
                products=["A1T1C1", "G1"],
                reaction_type=ReactionType.CATALYSIS,
                catalysts=["genesis_template"],
                activation_energy=25.0,
                heat_released=35.0,
                conditions={"event_bus": "available"},
            )
        )

        # Handle Command Codon: C → A → G (Sacred pattern to change the world)
        self.register_reaction(
            ChemicalReaction(
                name="handle_command_codon",
                reactants=["C1", "A1", "G1"],
                products=["CommandHandler(C1A1G1)"],
                sacred_codon=SacredCodon.HANDLE_COMMAND,
                reaction_type=ReactionType.SYNTHESIS,
                activation_energy=40.0,
                heat_released=25.0,
                conditions={"pattern": "C→A→G", "purpose": "change_state"},
            )
        )

        # Query Data Codon: C → T → C (Sacred pattern to see the world)
        self.register_reaction(
            ChemicalReaction(
                name="query_data_codon",
                reactants=["C1", "T1", "C1"],
                products=["QueryHandler(C1T1C1)"],
                sacred_codon=SacredCodon.QUERY_DATA,
                reaction_type=ReactionType.SYNTHESIS,
                activation_energy=35.0,
                heat_released=20.0,
                conditions={"pattern": "C→T→C", "purpose": "read_state"},
            )
        )

        # React to Event Codon: G → C → A → G (Sacred pattern to listen to the world)
        self.register_reaction(
            ChemicalReaction(
                name="react_to_event_codon",
                reactants=["G1", "C1", "A1", "G1"],
                products=["EventHandler(G1C1A1G1)"],
                sacred_codon=SacredCodon.REACT_TO_EVENT,
                reaction_type=ReactionType.SYNTHESIS,
                activation_energy=45.0,
                heat_released=30.0,
                conditions={
                    "pattern": "G→C→A→G",
                    "purpose": "listen_and_react",
                    "event_bus": "available",
                },
            )
        )

        # Immune Response Codon: G → C → A → C (Sacred pattern to heal the world)
        self.register_reaction(
            ChemicalReaction(
                name="immune_response_codon",
                reactants=["G1", "C1", "A1", "C1"],
                products=["ImmuneCell(G1C1A1C1)"],
                sacred_codon=SacredCodon.IMMUNE_RESPONSE,
                catalysts=["beekeeper_wisdom"],
                reaction_type=ReactionType.SYNTHESIS,
                activation_energy=60.0,
                heat_released=45.0,
                conditions={
                    "pattern": "G→C→A→C",
                    "purpose": "heal_mutations",
                    "immunity": "active",
                },
            )
        )

        # Choreography Codon: Complex multi-step workflows (Sacred pattern to become)
        self.register_reaction(
            ChemicalReaction(
                name="choreography_codon",
                reactants=["G1", "C1", "A1", "T1", "G1", "C1"],
                products=["WorkflowOrchestrator(G1C1A1T1G1C1)"],
                sacred_codon=SacredCodon.CHOREOGRAPHY,
                catalysts=["royal_jelly", "beekeeper_wisdom"],
                reaction_type=ReactionType.POLYMERIZATION,
                activation_energy=85.0,
                heat_released=75.0,
                conditions={
                    "pattern": "multi_step",
                    "purpose": "orchestrate_becoming",
                    "complexity": "high",
                },
            )
        )

        # Microservice decomposition
        self.register_reaction(
            ChemicalReaction(
                name="monolith_decomposition",
                reactants=["Monolith(A5T8C3G2)"],
                products=[
                    "Service1(A1T2C1G1)",
                    "Service2(A1T3C1G1)",
                    "Service3(A3T3C1G0)",
                ],
                reaction_type=ReactionType.DECOMPOSITION,
                activation_energy=100.0,
                heat_released=85.0,
                conditions={"coupling": "loose", "cohesion": "high"},
            )
        )

    def register_reaction(self, reaction: ChemicalReaction):
        """Register a new chemical reaction"""
        self._known_reactions[reaction.name] = reaction
        print(f"🧪 Registered reaction: {reaction}")

    def find_possible_reactions(
        self, available_reactants: List[str], available_catalysts: List[str] = None
    ) -> List[ChemicalReaction]:
        """Find all possible reactions given available reactants"""
        possible = []

        for reaction in self._known_reactions.values():
            if self._can_react(
                reaction, available_reactants, available_catalysts or []
            ):
                possible.append(reaction)

        return possible

    def _can_react(
        self,
        reaction: ChemicalReaction,
        available_reactants: List[str],
        available_catalysts: List[str],
    ) -> bool:
        """Check if a reaction can occur with available materials"""

        # Parse and count required reactants
        required_counts = {}
        for reactant in reaction.reactants:
            required_counts[reactant] = required_counts.get(reactant, 0) + 1

        # Parse and count available reactants
        available_counts = {}
        for reactant in available_reactants:
            available_counts[reactant] = available_counts.get(reactant, 0) + 1

        # Check if we have enough of each required reactant
        for reactant, needed in required_counts.items():
            if available_counts.get(reactant, 0) < needed:
                return False

        # Check catalyst requirements
        for catalyst in reaction.catalysts:
            if (
                catalyst not in available_catalysts
                and catalyst not in self._available_catalysts
            ):
                return False

        return True

    def execute_reaction(
        self,
        reaction: ChemicalReaction,
        available_reactants: List[str],
        available_catalysts: List[str] = None,
        temperature: float = 298.0,
        pressure: float = 1.0,
    ) -> ReactionResult:
        """Execute a chemical reaction to create new components"""

        print(f"🔬 Executing reaction: {reaction.name}")
        print(f"   {reaction}")

        available_catalysts = available_catalysts or []

        # Check if reaction can proceed
        if not self._can_react(reaction, available_reactants, available_catalysts):
            return ReactionResult(
                success=False,
                products_created=[],
                energy_consumed=0,
                energy_released=0,
                side_effects=["Insufficient reactants or catalysts"],
            )

        # Calculate reaction kinetics
        catalyst_efficiency = self._calculate_catalyst_efficiency(
            reaction.catalysts, available_catalysts
        )
        activation_energy_modified = reaction.activation_energy / catalyst_efficiency

        # Check if conditions are met
        if not self._check_reaction_conditions(reaction, temperature, pressure):
            return ReactionResult(
                success=False,
                products_created=[],
                energy_consumed=activation_energy_modified,
                energy_released=0,
                side_effects=["Reaction conditions not met"],
            )

        # Execute the reaction
        products_created = reaction.products.copy()
        energy_consumed = activation_energy_modified
        energy_released = reaction.heat_released * catalyst_efficiency
        reaction_time = self._calculate_reaction_time(
            reaction, catalyst_efficiency, temperature
        )

        # Generate byproducts (realistic chemistry often has byproducts)
        byproducts = self._generate_byproducts(reaction, catalyst_efficiency)

        result = ReactionResult(
            success=True,
            products_created=products_created,
            energy_consumed=energy_consumed,
            energy_released=energy_released,
            byproducts=byproducts,
            reaction_time=reaction_time,
        )

        # Record reaction history
        self._reaction_history.append((reaction, result))

        print("✅ Reaction completed successfully!")
        print(f"   Products: {', '.join(products_created)}")
        print(f"   Energy released: {energy_released:.1f} kJ/mol")
        print(f"   Reaction time: {reaction_time:.2f}s")

        return result

    def _calculate_catalyst_efficiency(
        self, required_catalysts: List[str], available_catalysts: List[str]
    ) -> float:
        """Calculate catalyst efficiency multiplier"""
        if not required_catalysts:
            return 1.0

        total_efficiency = 1.0
        for catalyst in required_catalysts:
            if (
                catalyst in available_catalysts
                and catalyst in self._available_catalysts
            ):
                efficiency = self._available_catalysts[catalyst]["efficiency"]
                total_efficiency *= efficiency

        return total_efficiency

    def _check_reaction_conditions(
        self, reaction: ChemicalReaction, temperature: float, pressure: float
    ) -> bool:
        """Check if reaction conditions are satisfied"""
        conditions = reaction.conditions

        # Temperature requirements
        if "min_temperature" in conditions:
            if temperature < float(conditions["min_temperature"]):
                return False

        if "max_temperature" in conditions:
            if temperature > float(conditions["max_temperature"]):
                return False

        # Pressure requirements
        if "min_pressure" in conditions:
            if pressure < float(conditions["min_pressure"]):
                return False

        # Other architectural conditions are assumed to be met for now
        return True

    def _calculate_reaction_time(
        self, reaction: ChemicalReaction, catalyst_efficiency: float, temperature: float
    ) -> float:
        """Calculate reaction time based on kinetics"""
        # Arrhenius equation approximation
        base_time = 10.0  # Base reaction time in seconds

        # Higher activation energy = slower reaction
        energy_factor = reaction.activation_energy / 50.0

        # Higher temperature = faster reaction
        temp_factor = 298.0 / temperature

        # Catalysts speed up reactions
        catalyst_factor = 1.0 / catalyst_efficiency

        return base_time * energy_factor * temp_factor * catalyst_factor

    def _generate_byproducts(
        self, reaction: ChemicalReaction, catalyst_efficiency: float
    ) -> List[str]:
        """Generate realistic byproducts from reactions"""
        byproducts = []

        # Lower catalyst efficiency tends to create more byproducts
        if catalyst_efficiency < 1.5:
            if reaction.reaction_type == ReactionType.SYNTHESIS:
                byproducts.append("TechnicalDebt")
            elif reaction.reaction_type == ReactionType.DECOMPOSITION:
                byproducts.append("OrphanedCode")

        # Polymerization often creates waste
        if reaction.reaction_type == ReactionType.POLYMERIZATION:
            if catalyst_efficiency < 2.0:
                byproducts.append("ArchitecturalSpaghetti")

        return byproducts

    def balance_equation(self, reaction: ChemicalReaction) -> bool:
        """Check if the chemical equation is balanced (conservation of ATCG atoms)"""

        def count_atoms(compounds: List[str]) -> Dict[str, int]:
            """Count ATCG atoms in compounds"""
            total_counts = {"A": 0, "T": 0, "C": 0, "G": 0}

            for compound in compounds:
                # Simple parsing for now - could be more sophisticated
                for element in ["A", "T", "C", "G"]:
                    count = compound.count(element)
                    total_counts[element] += count

            return total_counts

        reactant_atoms = count_atoms(reaction.reactants)
        product_atoms = count_atoms(reaction.products)

        # Check conservation
        for element in ["A", "T", "C", "G"]:
            if reactant_atoms[element] != product_atoms[element]:
                print(f"⚠️ Equation not balanced: {element} atoms don't match")
                return False

        print(f"✅ Equation balanced: {reaction}")
        return True

    def suggest_synthesis_route(self, target_component: str) -> List[ChemicalReaction]:
        """Suggest a synthesis route to create a target component"""
        synthesis_route = []

        # Simple heuristic approach - could be more sophisticated with graph search
        for reaction in self._known_reactions.values():
            if target_component in reaction.products:
                synthesis_route.append(reaction)

        return synthesis_route

    def find_reactions_by_codon(
        self, sacred_codon: SacredCodon
    ) -> List[ChemicalReaction]:
        """Find all reactions that implement a specific Sacred Codon"""
        return [
            reaction
            for reaction in self._known_reactions.values()
            if reaction.sacred_codon == sacred_codon
        ]

    def validate_codon_pattern(self, reaction: ChemicalReaction) -> bool:
        """
        Validate that the reaction follows the Sacred Codon pattern from PATTERNS.md.

        Sacred Codon patterns:
        - Handle Command: C → A → G
        - Query Data: C → T → C
        - React to Event: G → C → A → G
        - Immune Response: G → C → A → C
        - Choreography: Complex multi-step patterns
        """
        if not reaction.sacred_codon:
            return True  # No pattern to validate

        reactants = reaction.reactants
        products = reaction.products

        if reaction.sacred_codon == SacredCodon.HANDLE_COMMAND:
            # Should follow C → A → G pattern
            expected_elements = ["C", "A", "G"]
            return all(any(elem in r for r in reactants) for elem in expected_elements)

        elif reaction.sacred_codon == SacredCodon.QUERY_DATA:
            # Should follow C → T → C pattern
            c_count = sum(r.count("C") for r in reactants)
            t_count = sum(r.count("T") for r in reactants)
            return c_count >= 2 and t_count >= 1

        elif reaction.sacred_codon == SacredCodon.REACT_TO_EVENT:
            # Should follow G → C → A → G pattern
            g_count = sum(r.count("G") for r in reactants)
            c_count = sum(r.count("C") for r in reactants)
            a_count = sum(r.count("A") for r in reactants)
            return g_count >= 2 and c_count >= 1 and a_count >= 1

        elif reaction.sacred_codon == SacredCodon.IMMUNE_RESPONSE:
            # Should follow G → C → A → C pattern
            g_count = sum(r.count("G") for r in reactants)
            c_count = sum(r.count("C") for r in reactants)
            a_count = sum(r.count("A") for r in reactants)
            return g_count >= 1 and c_count >= 2 and a_count >= 1

        elif reaction.sacred_codon == SacredCodon.CHOREOGRAPHY:
            # Complex multi-step - should have multiple different elements
            element_types = set()
            for reactant in reactants:
                for elem in ["A", "T", "C", "G"]:
                    if elem in reactant:
                        element_types.add(elem)
            return (
                len(element_types) >= 3
            )  # Should use at least 3 different ATCG elements

        return False

    def get_codon_statistics(self) -> Dict[str, int]:
        """Get statistics about Sacred Codon usage"""
        codon_counts = {}
        for codon in SacredCodon:
            codon_counts[codon.value] = len(self.find_reactions_by_codon(codon))

        # Add reactions without codon mapping
        unmapped = len(
            [r for r in self._known_reactions.values() if r.sacred_codon is None]
        )
        codon_counts["unmapped"] = unmapped

        return codon_counts

    def get_reaction_statistics(self) -> Dict[str, float]:
        """Get statistics about executed reactions"""
        if not self._reaction_history:
            return {}

        total_reactions = len(self._reaction_history)
        successful_reactions = sum(
            1 for _, result in self._reaction_history if result.success
        )

        total_energy_consumed = sum(
            result.energy_consumed for _, result in self._reaction_history
        )
        total_energy_released = sum(
            result.energy_released for _, result in self._reaction_history
        )

        avg_reaction_time = (
            sum(result.reaction_time for _, result in self._reaction_history)
            / total_reactions
        )

        return {
            "total_reactions": total_reactions,
            "success_rate": successful_reactions / total_reactions,
            "total_energy_consumed": total_energy_consumed,
            "total_energy_released": total_energy_released,
            "net_energy": total_energy_released - total_energy_consumed,
            "avg_reaction_time": avg_reaction_time,
        }


# Example usage
if __name__ == "__main__":
    engine = ReactionEngine()

    print("🧪 Available reactions:")
    for name, reaction in engine._known_reactions.items():
        print(f"  {name}: {reaction}")

    # Show Sacred Codon mapping
    print("\n🔮 Sacred Codon Mapping:")
    codon_stats = engine.get_codon_statistics()
    for codon, count in codon_stats.items():
        print(f"  {codon}: {count} reactions")

    print("\n🔬 Testing Sacred Codon reactions...")

    # Test Handle Command Codon
    print("\n1. Testing Handle Command Codon (C→A→G)...")
    handle_reactions = engine.find_reactions_by_codon(SacredCodon.HANDLE_COMMAND)
    if handle_reactions:
        reaction = handle_reactions[0]
        print(f"   Pattern validated: {engine.validate_codon_pattern(reaction)}")
        result = engine.execute_reaction(reaction, ["C1", "A1", "G1"], [])
        if result.success:
            print(f"   ✅ Created: {result.products_created}")

    # Test Query Data Codon
    print("\n2. Testing Query Data Codon (C→T→C)...")
    query_reactions = engine.find_reactions_by_codon(SacredCodon.QUERY_DATA)
    if query_reactions:
        reaction = query_reactions[0]
        print(f"   Pattern validated: {engine.validate_codon_pattern(reaction)}")
        result = engine.execute_reaction(reaction, ["C1", "T1", "C1"], [])
        if result.success:
            print(f"   ✅ Created: {result.products_created}")

    # Test React to Event Codon
    print("\n3. Testing React to Event Codon (G→C→A→G)...")
    event_reactions = engine.find_reactions_by_codon(SacredCodon.REACT_TO_EVENT)
    if event_reactions:
        reaction = event_reactions[0]
        print(f"   Pattern validated: {engine.validate_codon_pattern(reaction)}")
        result = engine.execute_reaction(reaction, ["G1", "C1", "A1", "G1"], [])
        if result.success:
            print(f"   ✅ Created: {result.products_created}")

    # Test hexagonal formation
    print("\n4. Testing hexagonal architecture formation...")
    reactants = ["A", "C", "C", "C", "C", "C", "C"]
    catalysts = ["royal_jelly"]

    possible_reactions = engine.find_possible_reactions(reactants, catalysts)
    print(f"   Possible reactions: {len(possible_reactions)}")

    if possible_reactions:
        reaction = possible_reactions[0]
        result = engine.execute_reaction(reaction, reactants, catalysts)

        if result.success:
            print(f"   🎉 Successfully created: {result.products_created}")

    # Show final statistics
    print("\n📊 Final Statistics:")
    stats = engine.get_reaction_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
