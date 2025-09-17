"""
Bio/Sci Philosophy Aligned Adaptation Demo

This demonstrates the refactored Hive Adaptation Engine with bio/sci philosophy,
showing how the system now embraces organic evolution, beneficial mutations,
and symbiotic relationships rather than purely defensive responses.

Key Philosophy Changes:
- "Mutations" → "Adaptations" (neutral/beneficial framing)
- "Contamination" → "Evolution" (growth-oriented language)
- "Quarantine" → "Cultivation" (nurturing approach)
- "Severity" → "Fitness" (natural selection metaphor)
- "Emergency Response" → "Symbiotic Learning" (collaborative adaptation)
"""

import uuid
from typing import List, Dict, Any
from datetime import datetime, timezone
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp
from dna_core.pollen_protocol_pb2 import PollenEnvelope
from dna_core.royal_jelly import (
    SacredAggregate,
    SacredCommand,
    SacredCodonType,
    create_sacred_command,
    AdaptationType,
    get_adaptation_engine,
    process_event_with_adaptation_engine,
)


class BiophilicHelloHive(SacredAggregate):
    """
    HelloHive Aggregate designed with bio/sci philosophy principles.

    This aggregate demonstrates:
    - Organic adaptation to environmental changes
    - Beneficial mutation cultivation
    - Symbiotic relationships with other organisms
    - Natural selection of beneficial patterns
    - Evolutionary pressure responses

    Philosophy: "Every change is an opportunity for growth and adaptation"
    """

    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
        self.greeting_count = 0
        self.evolutionary_adaptations = []
        self.symbiotic_relationships = {}
        self.organism_health = "thriving"
        self.adaptation_fitness_score = 1.0

        # Configure for bio/sci philosophy
        self._configure_biophilic_adaptation()

    def create_adaptive_greeting(
        self, greeting_data: Dict[str, Any]
    ) -> List[PollenEnvelope]:
        """
        Create a greeting that can adapt and evolve over time.

        Bio/Sci Principle: Every interaction is a chance for beneficial mutation
        and evolutionary adaptation.
        """
        print(f"\n🌱 Creating adaptive greeting for organism {self.id}")

        # Create an evolutionary command
        command = create_sacred_command(
            command_type="create_adaptive_greeting",
            payload={
                **greeting_data,
                "evolutionary_potential": True,
                "symbiosis_enabled": True,
                "adaptation_timestamp": datetime.now(timezone.utc).isoformat(),
            },
            codon_type=SacredCodonType.HANDLE_COMMAND,
            source="biophilic_greeting_organism",
        )

        # Execute with natural adaptation monitoring
        events = self.execute_handle_command_codon(command)

        # Report organism health
        adaptation_status = self.get_organism_adaptation_status()
        print(f"🧬 Organism adaptation status: {adaptation_status['health']}")
        print(f"   Fitness score: {adaptation_status['fitness_score']:.2f}")
        print(
            f"   Beneficial adaptations: {adaptation_status['beneficial_adaptations']}"
        )

        return events

    def simulate_beneficial_evolution(
        self, evolution_type: str = "innovative"
    ) -> List[PollenEnvelope]:
        """
        Simulate beneficial evolutionary adaptations to demonstrate bio/sci philosophy.

        Unlike the previous "mutation simulation", this focuses on positive
        evolutionary changes that enhance organism capabilities.
        """
        print(f"\n🧬 Simulating beneficial {evolution_type} evolution")

        if evolution_type == "innovative":
            # Create event showcasing innovation adaptation
            evolved_event = PollenEnvelope(
                event_id=str(uuid.uuid4()),
                event_type="InnovativeGreetingEvolved",
                event_version="2.1",  # Evolved version
                aggregate_id=self.id,
                timestamp=self._create_timestamp(),
                payload=self._create_payload(
                    {
                        "message": "Hello with evolved capabilities!",
                        "innovation_type": "enhanced_communication",
                        "evolutionary_advantage": "increased_connection_quality",
                        "fitness_improvement": 0.8,
                    }
                ),
            )

        elif evolution_type == "adaptive":
            # Create event showing environmental adaptation
            evolved_event = PollenEnvelope(
                event_id=str(uuid.uuid4()),
                event_type="AdaptiveResponseEvolved",
                event_version="1.2",
                aggregate_id=self.id,
                timestamp=self._create_timestamp(),
                payload=self._create_payload(
                    {
                        "message": "Greeting adapted to new environment",
                        "adaptation_trigger": "environmental_change",
                        "survival_advantage": "better_context_awareness",
                    }
                ),
            )

        elif evolution_type == "symbiotic":
            # Create event demonstrating symbiotic evolution
            evolved_event = PollenEnvelope(
                event_id=str(uuid.uuid4()),
                event_type="SymbioticRelationshipEvolved",
                event_version="1.0",
                aggregate_id=self.id,
                timestamp=self._create_timestamp(),
                payload=self._create_payload(
                    {
                        "message": "Collaborative greeting with other organisms",
                        "symbiosis_type": "mutually_beneficial",
                        "partner_organisms": ["other_hive_components"],
                        "collective_fitness": 0.9,
                    }
                ),
            )

        else:
            # Generic evolutionary experiment
            evolved_event = PollenEnvelope(
                event_id=str(uuid.uuid4()),
                event_type="NewEvolutionaryExperiment",
                event_version="1.0",
                aggregate_id=self.id,
                timestamp=self._create_timestamp(),
                payload=self._create_payload(
                    {
                        "experiment_type": evolution_type,
                        "hypothesis": "exploring_new_adaptation_pathways",
                    }
                ),
            )

        # Process through adaptation engine
        adaptation_commands = process_event_with_adaptation_engine(evolved_event, self)

        print("🔬 Bio/Sci adaptation analysis complete:")
        print(f"   Adaptation opportunities detected: {len(adaptation_commands)}")

        # Embrace the adaptations via Sacred Codon patterns
        if adaptation_commands:
            print("🌿 Embracing evolutionary adaptations via Sacred Codon patterns")
            adaptation_events = []
            for command in adaptation_commands:
                # Convert adaptation commands to beneficial evolutionary events
                beneficial_event = self._create_beneficial_evolution_event(
                    command, evolved_event
                )
                adaptation_events.append(beneficial_event)
            return adaptation_events
        else:
            print("✨ Organism is already optimally adapted")
            return [evolved_event]

    def demonstrate_symbiotic_collaboration(self) -> Dict[str, Any]:
        """
        Demonstrate how this organism can form symbiotic relationships
        with other components in the Hive ecosystem.

        Bio/Sci Principle: Collaboration and mutualism drive evolution
        """
        print("\n🤝 Initiating symbiotic collaboration protocols")

        # Simulate symbiotic relationship formation
        partner_organisms = ["chronicler_bee", "pollen_processor", "queen_orchestrator"]

        symbiotic_benefits = {}
        for partner in partner_organisms:
            # Calculate mutual benefits
            fitness_gain = 0.1 + (len(partner) * 0.02)  # Simple fitness calculation

            symbiotic_benefits[partner] = {
                "relationship_type": "mutually_beneficial",
                "fitness_contribution": fitness_gain,
                "resource_sharing": True,
                "information_exchange": True,
                "collective_intelligence": True,
            }

            # Record in organism's symbiotic registry
            self.symbiotic_relationships[partner] = symbiotic_benefits[partner]

        # Update organism fitness based on symbiotic relationships
        symbiotic_fitness_bonus = sum(
            rel["fitness_contribution"] for rel in symbiotic_benefits.values()
        )
        self.adaptation_fitness_score += symbiotic_fitness_bonus

        print(f"🌱 Symbiotic relationships established: {len(symbiotic_benefits)}")
        print(f"🧬 Organism fitness improved: +{symbiotic_fitness_bonus:.2f}")

        return {
            "symbiotic_partners": len(symbiotic_benefits),
            "fitness_improvement": symbiotic_fitness_bonus,
            "collective_health": "enhanced",
            "ecosystem_resilience": "increased",
            "partnerships": symbiotic_benefits,
        }

    def get_organism_adaptation_status(self) -> Dict[str, Any]:
        """
        Get comprehensive adaptation status using bio/sci terminology.

        Replaces harsh "immune status" with nurturing "adaptation status"
        """
        # Get adaptation engine statistics
        try:
            engine = get_adaptation_engine()
            adaptation_stats = engine.get_adaptation_statistics()

            # Filter adaptations for this organism
            organism_adaptations = [
                a
                for a in engine.get_adaptation_history()
                if a.source_organism == self.id
            ]

            beneficial_adaptations = [a for a in organism_adaptations if a.beneficial]

        except Exception:
            adaptation_stats = {"error": "adaptation_engine_unavailable"}
            beneficial_adaptations = []

        return {
            "organism_id": self.id,
            "health": self.organism_health,
            "fitness_score": self.adaptation_fitness_score,
            "total_adaptations": len(self.evolutionary_adaptations),
            "beneficial_adaptations": len(beneficial_adaptations),
            "symbiotic_relationships": len(self.symbiotic_relationships),
            "adaptation_engine_stats": adaptation_stats,
            "evolutionary_potential": "high",
            "ecosystem_role": "collaborative_contributor",
        }

    def _configure_biophilic_adaptation(self):
        """Configure the organism for bio/sci philosophy adaptation"""
        try:
            engine = get_adaptation_engine()

            # Register custom beneficial adaptation sensor
            def sense_beneficial_greeting_evolution(event: PollenEnvelope) -> List:
                from dna_core.royal_jelly.immune_event_processor import AdaptationEvent

                adaptations = []

                # Look for positive evolutionary indicators
                if (
                    event.event_type.startswith("HelloHive")
                    or "Greeting" in event.event_type
                ):
                    payload_dict = dict(event.payload) if event.payload else {}

                    # Check for beneficial evolution patterns
                    beneficial_patterns = [
                        "innovative",
                        "evolved",
                        "adaptive",
                        "enhanced",
                        "improved",
                        "collaborative",
                        "symbiotic",
                    ]

                    message = payload_dict.get("message", "")
                    for pattern in beneficial_patterns:
                        if pattern.lower() in message.lower():
                            # High fitness for beneficial patterns
                            adaptations.append(
                                AdaptationEvent(
                                    adaptation_id=str(uuid.uuid4()),
                                    adaptation_type=AdaptationType.MESSAGE_EVOLUTION,
                                    fitness=0.8,  # High fitness for beneficial evolution
                                    description=f"Beneficial evolution pattern: {pattern}",
                                    source_event=event,
                                    source_organism=event.aggregate_id,
                                    observed_at=datetime.now(timezone.utc),
                                    evidence={
                                        "beneficial_pattern": pattern,
                                        "message": message,
                                    },
                                    evolutionary_pressure="positive_selection_pressure",
                                    beneficial=True,
                                )
                            )

                return adaptations

            engine.register_custom_sensor(sense_beneficial_greeting_evolution)
            print(f"🔬 Configured biophilic adaptation for organism {self.id}")

        except Exception as e:
            print(f"🌿 Note: Biophilic adaptation configuration needs adjustment: {e}")

    def _create_beneficial_evolution_event(
        self, adaptation_command: SacredCommand, original_event: PollenEnvelope
    ) -> PollenEnvelope:
        """Create an event representing beneficial evolutionary adaptation"""
        return PollenEnvelope(
            event_id=str(uuid.uuid4()),
            event_type="BeneficialAdaptationCultivated",
            event_version="1.0",
            aggregate_id=self.id,
            timestamp=self._create_timestamp(),
            payload=self._create_payload(
                {
                    "adaptation_command": adaptation_command.command_type,
                    "original_evolution": original_event.event_type,
                    "cultivation_result": "beneficial_trait_enhanced",
                    "fitness_improvement": True,
                    "ecosystem_contribution": "positive",
                }
            ),
        )

    def _create_timestamp(self) -> Timestamp:
        """Helper to create protobuf timestamp"""
        timestamp = Timestamp()
        timestamp.FromDatetime(datetime.now(timezone.utc))
        return timestamp

    def _create_payload(self, data: Dict[str, Any]) -> Struct:
        """Helper to create protobuf payload"""
        payload = Struct()
        payload.update(data)
        return payload

    # Implementation of Sacred Codon abstract methods with bio/sci focus

    def _execute_command_logic(self, command: SacredCommand) -> List[PollenEnvelope]:
        """Execute business logic with organic adaptation focus"""
        if command.command_type in ["create_greeting", "create_adaptive_greeting"]:
            return self._create_adaptive_greeting_logic(command)
        else:
            raise ValueError(f"Unknown command type: {command.command_type}")

    def _create_adaptive_greeting_logic(
        self, command: SacredCommand
    ) -> List[PollenEnvelope]:
        """Business logic for creating adaptive greetings"""
        greeting_data = command.payload

        # Update organism state with evolutionary awareness
        self.greeting_count += 1
        self.evolutionary_adaptations.append(
            {
                "adaptation_type": "greeting_evolution",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "evolutionary_pressure": greeting_data.get(
                    "evolutionary_pressure", "social_interaction"
                ),
            }
        )

        # Create evolutionary greeting event
        greeting_event = PollenEnvelope(
            event_id=str(uuid.uuid4()),
            event_type="AdaptiveGreetingEvolved",
            event_version="1.0",
            aggregate_id=self.id,
            timestamp=self._create_timestamp(),
            payload=self._create_payload(
                {
                    "message": greeting_data.get("message"),
                    "sender": greeting_data.get("sender", "unknown_organism"),
                    "evolution_generation": self.greeting_count,
                    "adaptation_potential": True,
                    "symbiotic_enabled": greeting_data.get("symbiosis_enabled", False),
                    "command_id": command.command_id,
                }
            ),
        )

        return [greeting_event]


def demonstrate_bio_sci_philosophy_alignment():
    """
    Comprehensive demonstration of bio/sci philosophy alignment
    in the refactored Hive Adaptation Engine.
    """

    print("🧬🌿 Bio/Sci Philosophy Alignment Demonstration")
    print("=" * 80)
    print("Philosophy: Embrace adaptation, cultivate beneficial evolution,")
    print("           foster symbiotic relationships, support natural selection")
    print()

    # Create biophilic organism
    bio_organism = BiophilicHelloHive("bio-hive-organism-001")

    print("📊 Initial Organism Status:")
    initial_status = bio_organism.get_organism_adaptation_status()
    print(f"   Health: {initial_status['health']}")
    print(f"   Fitness Score: {initial_status['fitness_score']:.2f}")
    print(f"   Evolutionary Potential: {initial_status['evolutionary_potential']}")

    # 1. Demonstrate adaptive greeting creation
    print("\n1. 🌱 Adaptive Greeting Creation (Organic Growth)")
    adaptive_events = bio_organism.create_adaptive_greeting(
        {
            "message": "Hello, evolving Hive ecosystem!",
            "sender": "BiophilicOrganism",
            "evolutionary_pressure": "communication_optimization",
            "symbiosis_enabled": True,
        }
    )
    print(f"   Generated {len(adaptive_events)} evolutionary events")

    # 2. Demonstrate beneficial evolution types
    evolution_types = ["innovative", "adaptive", "symbiotic"]

    for i, evolution_type in enumerate(evolution_types, 2):
        print(f"\n{i}. 🧬 {evolution_type.title()} Evolution Demonstration")
        evolution_events = bio_organism.simulate_beneficial_evolution(evolution_type)
        print(f"   Evolutionary adaptations: {len(evolution_events)}")

    # 3. Demonstrate symbiotic collaboration
    print("\n5. 🤝 Symbiotic Collaboration Formation")
    symbiosis_results = bio_organism.demonstrate_symbiotic_collaboration()
    print(f"   Symbiotic partners: {symbiosis_results['symbiotic_partners']}")
    print(f"   Fitness improvement: +{symbiosis_results['fitness_improvement']:.2f}")
    print(f"   Ecosystem resilience: {symbiosis_results['ecosystem_resilience']}")

    # 4. Final organism assessment
    print("\n📊 Final Organism Assessment:")
    final_status = bio_organism.get_organism_adaptation_status()
    print(f"   Health: {final_status['health']}")
    print(f"   Fitness Score: {final_status['fitness_score']:.2f}")
    print(f"   Total Adaptations: {final_status['total_adaptations']}")
    print(f"   Beneficial Adaptations: {final_status['beneficial_adaptations']}")
    print(f"   Symbiotic Relationships: {final_status['symbiotic_relationships']}")

    # 5. Compare with global adaptation engine
    print("\n🔬 Global Hive Adaptation Engine Status:")
    try:
        engine = get_adaptation_engine()
        global_stats = engine.get_adaptation_statistics()
        print(
            f"   Total Ecosystem Adaptations: {global_stats.get('total_adaptations', 0)}"
        )
        print(
            f"   Beneficial Adaptations: {global_stats.get('beneficial_adaptations', 0)}"
        )
        print(
            f"   Adaptation Efficiency: {global_stats.get('adaptation_efficiency', 0.0):.2f}"
        )
        print(f"   Symbiosis Enabled: {global_stats.get('symbiosis_enabled', False)}")
    except Exception as e:
        print(f"   Adaptation engine status: {e}")

    print("\n🌟 Bio/Sci Philosophy Demonstration Summary:")
    print("   ✅ Replaced 'mutation' with 'adaptation' (positive framing)")
    print("   ✅ Replaced 'contamination' with 'evolution' (growth-oriented)")
    print("   ✅ Replaced 'quarantine' with 'cultivation' (nurturing)")
    print("   ✅ Replaced 'severity' with 'fitness' (natural selection)")
    print("   ✅ Added symbiotic relationship capabilities")
    print("   ✅ Emphasized beneficial evolutionary adaptations")
    print("   ✅ Created organic, nature-inspired language throughout")

    print("\n🧬 The Hive now truly embodies bio/sci philosophy:")
    print("   • Embraces change as opportunity for growth")
    print("   • Cultivates beneficial adaptations")
    print("   • Fosters collaborative, symbiotic relationships")
    print("   • Applies natural selection for fitness optimization")
    print("   • Uses organic, biological terminology")

    return bio_organism


if __name__ == "__main__":
    demonstrate_bio_sci_philosophy_alignment()
