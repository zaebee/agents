import json
from typing import Dict, Any, List

from .metric_collector import MetricCollector
from dna_core.royal_jelly.mind import HiveMind
from dna_core.pollen_protocol_pb2 import WaggleDanceEvent, GenomeMessage
from dna_core.royal_jelly.organism import DigitalOrganism
from dna_core.royal_jelly.fitness import FitnessJudge
from dna_core.royal_jelly.nectar_quality import NectarQuality

class BeekeeperOperator:
    """
    The main operator that connects the production environment to the HiveMind.
    It orchestrates the observe-decide-act loop for self-healing and optimization.
    """

    def __init__(self):
        self.collector = MetricCollector()
        self.mind = HiveMind()
        self.fitness_judge = FitnessJudge() # The beekeeper uses the judge
        print("🤖 Humean Beekeeper Operator is online.")

    def run_simulation_cycle(self, simulator):
        """Runs a single tick of the simulation and checks for discoveries."""
        simulator.run_tick()

        # Run breeding contest if it's time
        if simulator.current_tick > 0 and simulator.current_tick % 10 == 0:
            newly_born = self.run_breeding_contest(simulator)
            if newly_born:
                self.check_for_discoveries(newly_born, simulator)

    def run_breeding_contest(self, simulator) -> List[DigitalOrganism]:
        """Selects the fittest organisms and allows them to replicate."""
        print(f"\n--- 🏆 Breeding Contest at Tick {simulator.current_tick} 🏆 ---")
        newly_born = []
        if not simulator.organisms:
            print("  Colony has died out. No contest.")
            return newly_born

        fittest_bees = sorted(simulator.organisms.values(), key=lambda o: o.fitness_score, reverse=True)
        breeder_count = max(1, len(fittest_bees) // 5)
        breeders = fittest_bees[:breeder_count]

        print(f"  Top {len(breeders)} bees selected for replication based on fitness.")
        for bee in breeders:
            cost_of_new_bee = 100
            if simulator.royal_jelly_bank >= cost_of_new_bee:
                print(f"    - Breeder: {bee.id} (Fitness: {bee.fitness_score:.2f})")
                child = bee.replicate()
                simulator.add_organism(child)
                simulator.royal_jelly_bank -= cost_of_new_bee
                newly_born.append(child)
            else:
                print(f"    - Hive cannot afford to sponsor new bee from {bee.id}.")
        return newly_born

    def check_for_discoveries(self, children: List[DigitalOrganism], simulator):
        """Checks if any new children have made a discovery worthy of a waggle dance."""
        for child in children:
            if self.should_dance(child, simulator):
                print(f"  -> ✨ Significant discovery! Child {child.id} is performing the waggle dance.")
                self.broadcast_waggle_dance(child, simulator)

    def should_dance(self, organism: DigitalOrganism, simulator) -> bool:
        """Implements the intelligent triggers for the Waggle Dance Protocol."""
        # 1. Genome Fitness Trigger: Is the bee's DNA exceptionally good?
        genome_fitness = self.fitness_judge.calculate_genome_fitness(organism.genome)
        if genome_fitness > 90:
            print(f"    - Dance Reason: Superior Genome (Fitness: {genome_fitness:.2f})")
            return True

        # 2. Nectar Quality Trigger is not implemented in this experiment
        # but would be a valid trigger in a more complex scenario.

        # 3. Novelty Trigger (Simulated)
        if "novel_trait_xyz" in organism.genome.traits:
            print(f"    - Dance Reason: Novel Trait Discovered.")
            return True

        return False

    def broadcast_waggle_dance(self, organism: DigitalOrganism, simulator):
        """Constructs and 'broadcasts' a WaggleDanceEvent."""
        avg_fitness = simulator.mind.global_metrics.get("average_fitness", 0)

        genome_msg = GenomeMessage(
            primitive_type=organism.genome.primitive_type.name,
            purpose=organism.genome.purpose,
            nectar_production_rate=organism.genome.nectar_production_rate
        )

        event = WaggleDanceEvent(
            source_hive_id="beekeeper-01",
            source_component_id=organism.id,
            fitness_score=self.fitness_judge.calculate_genome_fitness(organism.genome),
            fitness_delta=(self.fitness_judge.calculate_genome_fitness(organism.genome) - avg_fitness),
            genome=genome_msg
        )

        event_json = {
            "source_hive_id": event.source_hive_id,
            "source_component_id": event.source_component_id,
            "fitness_score": event.fitness_score,
            "genome": {
                "primitive_type": event.genome.primitive_type,
                "purpose": event.genome.purpose,
                "nectar_production_rate": event.genome.nectar_production_rate,
            }
        }
        print(f"  💃 BROADCASTING Waggle Dance: {json.dumps(event_json, indent=2)}")
        # In a real system, this would be published to an event bus.
        simulator.event_bus.append(event)
