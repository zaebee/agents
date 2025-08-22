import time
from typing import List, Dict

from dna_core.royal_jelly.organism import DigitalOrganism, Genome
from dna_core.royal_jelly.ethics import EthicalGovernor
from dna_core.royal_jelly.periodic_table import ElementSymbol


class TestBee(DigitalOrganism):
    """A simple, concrete implementation of a DigitalOrganism for testing."""

    def __init__(self):
        test_genome = Genome(
            primitive_type=ElementSymbol.A,
            bonds_template=("TestEvent",),
            valency=(1, 1),
            purpose="To test the Hive simulator."
        )
        super().__init__(test_genome)

    def main_function(self, event: Dict):
        """Processes a single event, consumes nectar, and logs the action."""
        print(f"  -> {self.id} processing event: {event.get('type')}")
        nectar_cost = 10
        self.metabolism.nectar_level -= nectar_cost
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
        self.event_bus: List[Dict] = [] # A simple list for now

        print(f"🌱 Hive Simulator initialized with {len(organisms)} organism(s).")
        print(f"   Max ticks: {self.max_ticks}")
        print(f"   Ethical Governor: {self.governor}")


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
    print("--- 🐝 Running the First Controlled Experiment 🐝 ---")

    # 1. Instantiate one TestBee
    bee = TestBee()

    # 2. Configure the simulator
    sim = HiveSimulator(max_ticks=20, organisms=[bee])

    # 3. Define the events to be fed to the bee
    events_to_feed = [
        {"tick": 2, "event": {"type": "TestEvent", "data": "A"}},
        {"tick": 4, "event": {"type": "TestEvent", "data": "B"}},
        {"tick": 6, "event": {"type": "TestEvent", "data": "C"}},
        {"tick": 8, "event": {"type": "TestEvent", "data": "D"}},
        {"tick": 10, "event": {"type": "TestEvent", "data": "E"}},
        {"tick": 12, "event": {"type": "TestEvent", "data": "F"}},
        {"tick": 14, "event": {"type": "TestEvent", "data": "G"}},
        {"tick": 16, "event": {"type": "TestEvent", "data": "H"}},
        {"tick": 18, "event": {"type": "TestEvent", "data": "I"}},
        {"tick": 20, "event": {"type": "TestEvent", "data": "J"}},
    ]
    event_idx = 0

    # 4. Run the simulation and feed events
    print("\n--- Simulation Starting ---")
    for i in range(sim.max_ticks):
        sim.current_tick = i + 1
        print(f"\n--- Tick {sim.current_tick}/{sim.max_ticks} ---")

        # Feed event if it's the right tick
        if event_idx < len(events_to_feed) and sim.current_tick == events_to_feed[event_idx]["tick"]:
            event_data = events_to_feed[event_idx]["event"]
            print(f"  * Feeding event {event_data['data']} to {bee.id}")
            bee.main_function(event_data)
            event_idx += 1

        # Process one tick for each organism
        for org_id, organism in list(sim.organisms.items()):
            organism.tick()
            print(f"  - Ticked {organism.id}. Age: {organism.metabolism.age}, Nectar: {organism.metabolism.nectar_level}")

            if organism.metabolism.age > sim.governor.max_age:
                sim.reap(organism.id, "old age")

        time.sleep(0.1)

    print("\n--- Simulation Finished ---")
    sim.print_summary()
    print("\n--- Experiment Complete ---")
