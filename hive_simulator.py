import time
from typing import List, Dict

from dna_core.royal_jelly.organism import DigitalOrganism, Genome, StarvationError
from dna_core.royal_jelly.ethics import EthicalGovernor
from dna_core.royal_jelly.periodic_table import ElementSymbol
from dna_core.royal_jelly.bonds import PlasticBonds
from dna_core.royal_jelly.fitness import FitnessJudge


class TestBee(DigitalOrganism):
    """A simple, concrete implementation of a DigitalOrganism for testing."""

    def __init__(self, genome: Genome = None, generation: int = 1, initial_nectar_prod_rate: int = 1):
        if genome is None:
            # Create a default genome if one isn't provided, using the initial rate.
            genome = Genome(
                primitive_type=ElementSymbol.A,
                bonds_template=("TestEvent",),
                valency=(1, 1),
                purpose="To test the Hive simulator.",
                nectar_production_rate=initial_nectar_prod_rate
            )
        super().__init__(genome=genome, generation=generation)


    def main_function(self, event: Dict):
        """Processes a single event, consumes nectar, and logs the action."""
        print(f"  -> {self.id} processing event: {event.get('type')}")
        nectar_cost = 25  # Increased cost to make starvation more likely
        self.consume_nectar(nectar_cost)
        self.event_log.append(event)
        print(f"     Consumed {nectar_cost} nectar. Current level: {self.metabolism.nectar_level}")


class HiveSimulator:
    """
    A controlled environment to simulate the life and evolution of DigitalOrganisms.
    This is the "nursery" where we can safely observe the behavior of our bees.
    """

    def __init__(self, max_ticks: int = 100, organisms: List[DigitalOrganism] = None):
        if organisms is None:
            organisms = []
        self.max_ticks: int = max_ticks
        self.organisms: Dict[str, DigitalOrganism] = {org.id: org for org in organisms}
        self.current_tick: int = 0
        self.governor: EthicalGovernor = EthicalGovernor()
        self.bonds: PlasticBonds = PlasticBonds()
        self.fitness_judge: FitnessJudge = FitnessJudge()
        self.royal_jelly_bank: float = 0.0
        self.tax_rate = 0.1 # 10% tax on nectar production
        self.event_bus: List[Dict] = [] # A simple list for now

        print(f"🌱 Hive Simulator initialized with {len(organisms)} organism(s).")
        print(f"   Max ticks: {self.max_ticks}")
        print(f"   Ethical Governor: {self.governor}")
        print(f"   Bond Manager: {self.bonds}")
        print(f"   Fitness Judge: Enabled")
        print(f"   Royal Jelly Bank: Enabled (Tax Rate: {self.tax_rate*100}%)")


    def run(self):
        """Runs the full simulation for the specified number of ticks."""
        print("\n--- Simulation Starting ---")
        for i in range(self.max_ticks):
            self.current_tick = i + 1
            print(f"\n--- Tick {self.current_tick}/{self.max_ticks} ---")

            # Process one tick for each organism
            for org_id, organism in list(self.organisms.items()):
                organism.tick()
                print(f"  - Ticked {organism.id}. Age: {organism.metabolism.age}, Nectar: {organism.metabolism.nectar_level}")

                # Simple check for apoptosis
                if organism.metabolism.age > self.governor.max_age:
                    self.reap(organism.id, "old age")

            time.sleep(0.1) # To make the simulation observable in real-time

        print("\n--- Simulation Finished ---")
        self.print_summary()

    def add_organism(self, organism: DigitalOrganism):
        """Adds a new organism to the simulation."""
        self.organisms[organism.id] = organism
        print(f"  + Added {organism.id} to the hive.")

    def reap(self, organism_id: str, reason: str):
        """Removes a dead organism from the simulation."""
        if organism_id in self.organisms:
            print(f"  - 💀 Reaping {organism_id} due to {reason}.")
            del self.organisms[organism_id]

    def print_summary(self):
        """Prints a summary of the final state of the hive."""
        print("\n--- Hive Summary ---")
        print(f"Total Ticks: {self.current_tick}")
        print(f"Surviving Organisms: {len(self.organisms)}")
        for org in self.organisms.values():
            print(f"  - {org}")
        print("--------------------")


if __name__ == "__main__":
    import random
    import numpy as np

    print("--- 🧬 Running the Directed Evolution Experiment 🧬 ---")

    # 1. Create an initial population with varied genetics
    initial_population = []
    for i in range(10):
        # Create bees with a range of nectar production rates
        prod_rate = random.randint(1, 20)
        bee = TestBee(initial_nectar_prod_rate=prod_rate)
        bee.id = f"Bee-Gen1-{i}"
        initial_population.append(bee)

    # 2. Configure the simulator
    sim = HiveSimulator(max_ticks=101, organisms=initial_population)

    # Calculate initial average fitness
    initial_avg_prod_rate = np.mean([o.metabolism.nectar_production_rate for o in sim.organisms.values()])
    print(f"\nInitial average nectar production rate: {initial_avg_prod_rate:.2f}")

    # 3. Run the simulation
    print("\n--- Simulation Starting ---")
    for i in range(sim.max_ticks):
        sim.current_tick = i + 1

        # Tick all organisms, apply tax, and calculate fitness
        for org_id, organism in list(sim.organisms.items()):
            nectar_before = organism.metabolism.nectar_level
            organism.tick()

            nectar_produced = (organism.metabolism.nectar_level - (nectar_before - 1))
            if nectar_produced > 0:
                tax = nectar_produced * sim.tax_rate
                organism.metabolism.nectar_level -= tax
                sim.royal_jelly_bank += tax

            organism.fitness_score = sim.fitness_judge.calculate_fitness(organism)
            print(f"  - Ticked {organism}")

            if organism.metabolism.age > sim.governor.max_age:
                sim.reap(organism.id, "old age")

        # Run breeding contest every 20 ticks
        if sim.current_tick > 0 and sim.current_tick % 20 == 0:
            print(f"\n--- 🏆 Breeding Contest at Tick {sim.current_tick} 🏆 ---")
            print(f"    (Royal Jelly Bank: {sim.royal_jelly_bank:.2f})")
            if not sim.organisms:
                print("  Colony has died out. No contest.")
                break

            fittest_bees = sorted(sim.organisms.values(), key=lambda o: o.fitness_score, reverse=True)

            breeder_count = max(1, len(fittest_bees) // 5)
            breeders = fittest_bees[:breeder_count]

            print(f"  Top {len(breeders)} bees selected for replication based on fitness.")
            for bee in breeders:
                cost_of_new_bee = 100
                if sim.royal_jelly_bank >= cost_of_new_bee:
                    print(f"    - Breeder: {bee.id} (Fitness: {bee.fitness_score:.2f})")
                    child = bee.replicate()
                    sim.add_organism(child)
                    sim.royal_jelly_bank -= cost_of_new_bee
                else:
                    print(f"    - Hive cannot afford to sponsor new bee from {bee.id}.")

        sim.bonds.decay_bonds()

    # 4. Verification and Visualization
    print("\n--- Simulation Finished ---")
    sim.print_summary()

    print("\n--- Verification of Evolution ---")
    if sim.organisms:
        final_avg_prod_rate = np.mean([o.metabolism.nectar_production_rate for o in sim.organisms.values()])
        print(f"Initial average nectar production rate: {initial_avg_prod_rate:.2f}")
        print(f"Final average nectar production rate:   {final_avg_prod_rate:.2f}")

        assert final_avg_prod_rate > initial_avg_prod_rate, "Evolution failed: average fitness did not increase."
        print("\n✅ Verification successful: The Hive has evolved towards higher nectar production.")
    else:
        print("Colony did not survive the experiment.")

    print("\n--- Experiment Complete ---")
