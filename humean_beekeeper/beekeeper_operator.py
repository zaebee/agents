import json
from typing import Dict, Any, List

from .metric_collector import MetricCollector
from dna_core.royal_jelly.mind import HiveMind
from dna_core.pollen_protocol_pb2 import WaggleDanceEvent, GenomeMessage
from dna_core.royal_jelly.organism import DigitalOrganism, Genome
from dna_core.royal_jelly.fitness import FitnessJudge
from dna_core.royal_jelly.nectar_quality import NectarQuality
from dna_core.royal_jelly.periodic_table import ElementSymbol
from hive_simulator import TestBee

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
        """Runs a single tick of the simulation, listens for news, and manages the hive."""
        # A beekeeper first observes the world, then its own hive, then acts.
        self.listen_for_foreign_dances(simulator)

        simulator.run_tick()

        # Run breeding contest if it's time
        if simulator.current_tick > 0 and simulator.current_tick % 10 == 0:
            newly_born = self.run_breeding_contest(simulator)
            if newly_born:
                self.check_for_discoveries(newly_born, simulator)

    def listen_for_foreign_dances(self, simulator):
        """
        Processes the event bus for dances from other hives and incorporates superior genomes.
        """
        # Ensure the mind has the latest metrics from its own hive first
        self.mind.observe(list(simulator.organisms.values()))
        avg_local_fitness = self.mind.global_metrics.get("average_fitness", 0)

        for event in simulator.event_bus:
            # Ensure we are looking at a WaggleDanceEvent from another hive
            if isinstance(event, WaggleDanceEvent) and event.source_hive_id != simulator.name:
                print(f"  [{simulator.name}] Heard a waggle dance from '{event.source_hive_id}'!")

                # Decision logic: is the foreign gene "better"?
                if event.fitness_score > avg_local_fitness:
                    print(f"    - Foreign genome is superior (Fitness: {event.fitness_score:.2f} > Local Avg: {avg_local_fitness:.2f}).")
                    self.adopt_foreign_genome(event, simulator)

    def adopt_foreign_genome(self, event: WaggleDanceEvent, simulator):
        """Creates a new organism from a foreign genome and adds it to the hive."""
        print(f"    - Action: Adopting foreign genome from {event.source_hive_id}.")

        foreign_genome_msg = event.genome
        try:
            primitive_type_enum = ElementSymbol[foreign_genome_msg.primitive_type]
        except KeyError:
            print(f"    - ⚠️ ERROR: Unknown primitive type '{foreign_genome_msg.primitive_type}' in event. Cannot adopt.")
            return

        reconstructed_genome = Genome(
            primitive_type=primitive_type_enum,
            purpose=foreign_genome_msg.purpose,
            nectar_production_rate=foreign_genome_msg.nectar_production_rate,
            bonds_template=("TestEvent",),
            valency=(1, 1),
            traits=("immigrant", "adopted")
        )

        immigrant_bee = TestBee(genome=reconstructed_genome)
        # Give the immigrant a unique ID based on its origin
        immigrant_bee.id = f"Immigrant-{event.source_component_id[:8]}"

        simulator.add_organism(immigrant_bee)

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
            source_hive_id=simulator.name, # Use the simulator's name for proper identification
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
