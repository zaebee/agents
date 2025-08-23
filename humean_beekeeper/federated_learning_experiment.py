import sys
import os

# Add project root to path before other imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from humean_beekeeper.beekeeper_operator import BeekeeperOperator
from hive_simulator import HiveSimulator, TestBee
from dna_core.royal_jelly.organism import Genome
from dna_core.royal_jelly.periodic_table import ElementSymbol

def setup_hives(shared_event_bus):
    """Creates two hives, one with a superior bee and one with average bees."""
    # 1. Create a truly "genius" Genome to ensure it passes the fitness threshold
    superior_genome = Genome(
        primitive_type=ElementSymbol.T,
        purpose="A highly efficient, caching, robust, O(1) transform.",
        nectar_production_rate=40,
        algorithm_complexity="O(1)",
        error_handling_level="robust",
        traits=("caching", "superior"),
        bonds_template=("TestEvent",),
        valency=(1, 1)
    )
    superior_bee = TestBee(genome=superior_genome)
    superior_bee.id = "SuperiorBee-Gen1"

    # 2. Create a standard, less efficient Genome
    average_genome = Genome(
        primitive_type=ElementSymbol.T,
        purpose="A standard, non-caching transform.",
        nectar_production_rate=5,
        traits=("standard",),
        bonds_template=("TestEvent",),
        valency=(1, 1)
    )
    average_bees = [TestBee(genome=average_genome, initial_nectar_prod_rate=5) for _ in range(3)]
    for i, bee in enumerate(average_bees):
        bee.id = f"AverageBee-{i+1}"

    # 3. Create the two simulators sharing the event bus
    alpha_sim = HiveSimulator(
        name="HiveAlpha",
        organisms=[superior_bee],
        event_bus=shared_event_bus
    )
    alpha_sim.royal_jelly_bank = 100.0

    beta_sim = HiveSimulator(
        name="HiveBeta",
        organisms=average_bees,
        event_bus=shared_event_bus
    )
    beta_sim.royal_jelly_bank = 100.0

    return alpha_sim, beta_sim

def main():
    """
    Main entry point for the Federated Learning Experiment.
    """
    print("--- 🐝 Initializing Federated Learning Experiment 🐝 ---")

    shared_event_bus = []
    alpha_sim, beta_sim = setup_hives(shared_event_bus)

    alpha_operator = BeekeeperOperator()
    beta_operator = BeekeeperOperator()

    print("\n--- Running simulation ---")
    for tick in range(20):
        print(f"\n--- Global Tick {tick+1} ---")
        print(f"--- {alpha_sim.name} ---")
        alpha_operator.run_simulation_cycle(alpha_sim)

        print(f"--- {beta_sim.name} ---")
        beta_operator.run_simulation_cycle(beta_sim)

    # 4. Verification
    print("\n--- Verification ---")
    print(f"Total events in shared bus: {len(shared_event_bus)}")

    # Check if HiveAlpha broadcasted at least one dance
    assert len(shared_event_bus) > 0, "❌ FAILED: HiveAlpha did not broadcast any waggle dances."
    print("✅ SUCCESS: At least one WaggleDanceEvent was broadcast.")

    # Check if HiveBeta adopted a foreign bee
    has_immigrant = any("immigrant" in bee.genome.traits for bee in beta_sim.organisms.values())
    assert has_immigrant, "❌ FAILED: HiveBeta did not adopt the superior foreign genome."
    print("✅ SUCCESS: HiveBeta successfully adopted a superior genome from HiveAlpha.")

    print("\n--- 🐝 Federated Learning Experiment Complete 🐝 ---")


if __name__ == "__main__":
    main()
