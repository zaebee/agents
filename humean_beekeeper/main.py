import sys
import os

# Add project root to path before other imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import io
import contextlib
from humean_beekeeper.beekeeper_operator import BeekeeperOperator
from hive_simulator import HiveSimulator, TestBee # Assuming these are in a file named hive_simulator.py
from dna_core.pollen_protocol_pb2 import WaggleDanceEvent, GenomeMessage
from dna_core.royal_jelly.organism import Genome
from dna_core.royal_jelly.periodic_table import ElementSymbol
from google.protobuf.json_format import Parse

def run_hive_simulation(operator, simulator, ticks):
    """Helper to run simulation and capture broadcast events."""
    for _ in range(ticks):
        operator.run_simulation_cycle(simulator)
    return simulator.event_bus

def main():
    """
    Main entry point for the Genome-First Protocol Test.
    """
    print("--- 🧬 Initializing Genome-First Protocol Experiment 🧬 ---")

    # 1. Create a bee with a genetically superior Genome
    superior_genome = Genome(
        primitive_type=ElementSymbol.T,
        bonds_template=(),
        valency=(1, 1),
        purpose="A highly efficient, caching transform.",
        nectar_production_rate=20,
        algorithm_complexity="O(1)",
        error_handling_level="robust",
        traits=("caching",)
    )
    superior_bee = TestBee(genome=superior_genome)
    superior_bee.id = "SuperiorBee-Gen1"

    # 2. Setup the operator and a simulator containing this one bee
    operator = BeekeeperOperator()
    simulator = HiveSimulator(organisms=[superior_bee])
    simulator.royal_jelly_bank = 100.0 # Pre-fund the hive to afford replication

    # 3. Run for 10 ticks to trigger a breeding contest. The Beekeeper should
    #    recognize the superior genome of the child and broadcast a waggle dance.
    print("\n--- Running simulation to test discovery ---")
    broadcasts = run_hive_simulation(operator, simulator, 10)

    # 4. Verification
    print("\n--- Verification ---")
    assert len(broadcasts) > 0, "❌ FAILED: The Beekeeper did not broadcast a waggle dance for the superior genome."

    dance = broadcasts[0]
    print(f"  -> Waggle dance was broadcast for genome from {dance.source_component_id}")
    assert dance.genome.primitive_type == "T"
    assert "caching" in dance.genome.purpose.lower()

    print("✅ SUCCESS: The new Waggle Dance trigger correctly identified and broadcast the superior genome.")
    print("\n--- 🐝 Genome-First Protocol Experiment Complete 🐝 ---")


if __name__ == "__main__":
    main()
