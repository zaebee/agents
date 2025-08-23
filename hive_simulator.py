import time
from typing import List, Dict
import random
import numpy as np
import io
import contextlib

from dna_core.royal_jelly.organism import DigitalOrganism, Genome, StarvationError
from dna_core.royal_jelly.ethics import EthicalGovernor
from dna_core.royal_jelly.periodic_table import ElementSymbol
from dna_core.royal_jelly.bonds import PlasticBonds
from dna_core.royal_jelly.fitness import FitnessJudge
from dna_core.royal_jelly.mind import HiveMind


class TestBee(DigitalOrganism):
    """A simple, concrete implementation of a DigitalOrganism for testing."""
    def __init__(self, genome: Genome = None, generation: int = 1, initial_nectar_prod_rate: int = 1):
        if genome is None:
            genome = Genome(
                primitive_type=ElementSymbol.A,
                bonds_template=("TestEvent",),
                valency=(1, 1),
                purpose="To test the Hive simulator.",
                nectar_production_rate=initial_nectar_prod_rate
            )
        super().__init__(genome=genome, generation=generation)

    def main_function(self, event: Dict):
        print(f"  -> {self.id} processing event: {event.get('type')}")
        nectar_cost = 25
        self.consume_nectar(nectar_cost)
        self.event_log.append(event)
        print(f"     Consumed {nectar_cost} nectar. Current level: {self.metabolism.nectar_level}")


class HiveSimulator:
    """A controlled environment to simulate the life and evolution of DigitalOrganisms."""
    def __init__(self, max_ticks: int = 100, organisms: List[DigitalOrganism] = None):
        if organisms is None:
            organisms = []
        self.max_ticks: int = max_ticks
        self.organisms: Dict[str, DigitalOrganism] = {org.id: org for org in organisms}
        self.current_tick: int = 0
        self.governor: EthicalGovernor = EthicalGovernor()
        self.bonds: PlasticBonds = PlasticBonds()
        self.fitness_judge: FitnessJudge = FitnessJudge()
        self.mind: HiveMind = HiveMind()
        self.royal_jelly_bank: float = 0.0
        self.tax_rate = 0.1
        self.event_bus: List[Dict] = []
        self.born_in_tick: Dict[int, List[DigitalOrganism]] = {}

    def run_tick(self) -> None:
        """
        Runs a single tick of the simulation.
        This method is now orchestrated by the BeekeeperOperator.
        It no longer creates organisms; it only advances their state.
        """
        self.current_tick += 1
        print(f"\n--- Tick {self.current_tick}/{self.max_ticks} ---")

        self.mind.observe(list(self.organisms.values()))

        for org_id, organism in list(self.organisms.items()):
            nectar_before = organism.metabolism.nectar_level
            organism.tick()

            nectar_produced = (organism.metabolism.nectar_level - (nectar_before - 1))
            if nectar_produced > 0:
                tax = nectar_produced * self.tax_rate
                organism.metabolism.nectar_level -= tax
                self.royal_jelly_bank += tax

            # The Beekeeper is now responsible for judging fitness before a contest
            organism.fitness_score = self.fitness_judge.calculate_genome_fitness(organism.genome)
            print(f"  - Ticked {organism}")

            if organism.metabolism.age > self.governor.max_age:
                self.reap(organism.id, "old age")

        self.bonds.decay_bonds()
        time.sleep(0.01)

    def add_organism(self, organism: DigitalOrganism):
        self.organisms[organism.id] = organism
        print(f"  + Added {organism.id} to the hive.")

    def reap(self, organism_id: str, reason: str):
        if organism_id in self.organisms:
            print(f"  - 💀 Reaping {organism_id} due to {reason}.")
            del self.organisms[organism_id]

    def print_summary(self):
        print("\n--- Hive Summary ---")
        print(f"Total Ticks: {self.current_tick}")
        print(f"Surviving Organisms: {len(self.organisms)}")
        for org in self.organisms.values():
            print(f"  - {org}")
        print("--------------------")

if __name__ == "__main__":
    print("This file is not meant to be run directly anymore.")
    print("Please run `humean_beekeeper/main.py` to see the experiment.")
