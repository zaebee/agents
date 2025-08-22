import time
from typing import List, Dict

from dna_core.royal_jelly.organism import DigitalOrganism, Genome, StarvationError
from dna_core.royal_jelly.ethics import EthicalGovernor
from dna_core.royal_jelly.periodic_table import ElementSymbol
from dna_core.royal_jelly.bonds import PlasticBonds


class TestBee(DigitalOrganism):
    """A simple, concrete implementation of a DigitalOrganism for testing."""

    def __init__(self, genome: Genome = None, nectar_production_rate: int = 1, generation: int = 1):
        if genome is None:
            # Create a default genome if one isn't provided
            genome = Genome(
                primitive_type=ElementSymbol.A,
                bonds_template=("TestEvent",),
                valency=(1, 1),
                purpose="To test the Hive simulator."
            )
        super().__init__(genome=genome, generation=generation)
        self.metabolism.nectar_production_rate = nectar_production_rate


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
        self.event_bus: List[Dict] = [] # A simple list for now

        print(f"🌱 Hive Simulator initialized with {len(organisms)} organism(s).")
        print(f"   Max ticks: {self.max_ticks}")
        print(f"   Ethical Governor: {self.governor}")
        print(f"   Bond Manager: {self.bonds}")


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
    print("--- 🧠 Running the Learning and Inheritance Experiment 🧠 ---")

    # 1. Create the initial bees
    parent_bee = TestBee(nectar_production_rate=50)
    parent_bee.id = "ParentBee-Gen1"

    partner_bee = TestBee(nectar_production_rate=10)
    partner_bee.id = "PartnerBee"

    # 2. Configure the simulator
    sim = HiveSimulator(max_ticks=30, organisms=[parent_bee, partner_bee])

    # 3. Scenario setup
    child_id = None

    # 4. Run the simulation
    print("\n--- Simulation Starting ---")
    for i in range(sim.max_ticks):
        sim.current_tick = i + 1
        print(f"\n--- Tick {sim.current_tick}/{sim.max_ticks} ---")

        # Scenario events
        if sim.current_tick == 5:
            print(f"  * Parent bee encounters a 'WisdomFlower'.")
            parent_bee.learn_engram("nectar_source_efficiency", 0.8)

        if sim.current_tick == 10:
            print(f"  * Parent bee interacts with Partner bee.")
            sim.bonds.record_interaction(parent_bee.id, partner_bee.id, strength=5.0)

        # Tick all organisms
        for org_id, organism in list(sim.organisms.items()):
            organism.tick()
            print(f"  - Ticked {organism.id}. Age: {organism.metabolism.age}, Nectar: {organism.metabolism.nectar_level}")

            # Check for replication
            if organism.id == parent_bee.id and organism.metabolism.nectar_level > sim.governor.replication_threshold:
                if sim.governor.check_action(organism, "replicate"):
                    child = organism.replicate()
                    child_id = child.id
                    sim.add_organism(child)
                    organism.metabolism.nectar_level //= 2

        sim.bonds.decay_bonds()
        time.sleep(0.05)

    # 5. Verification and Visualization
    print("\n--- Simulation Finished ---")
    sim.print_summary()

    print("\n--- Verification ---")
    # Verify bond strength
    bond_strength = sim.bonds.get_bond_strength(parent_bee.id, partner_bee.id)
    print(f"Final bond strength between Parent and Partner: {bond_strength:.2f}")
    assert bond_strength > 1.0, "Bond did not strengthen correctly!"

    # Verify inheritance
    if child_id and child_id in sim.organisms:
        child_bee = sim.organisms[child_id]
        parent_engram = parent_bee.epigenome.engrams.get("nectar_source_efficiency")
        child_engram = child_bee.epigenome.engrams.get("nectar_source_efficiency")
        print(f"Parent's learned engram: {parent_engram}")
        print(f"Child's inherited engram: {child_engram}")
        assert parent_engram == child_engram, "Child did not inherit engram!"
        print("✅ Verification successful: Child inherited wisdom.")
    else:
        print("❌ Verification failed: Child bee was not created or did not survive.")

    print("\n--- Experiment Complete ---")
