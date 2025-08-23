import sys
import os
import shutil
import pathlib

# Add project root to path before other imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from humean_beekeeper.beekeeper_operator import BeekeeperOperator
from humean_beekeeper.federated_learning_experiment import setup_hives
import runpy
import re

def to_snake_case(name: str) -> str:
    """Converts a name to snake_case."""
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower().replace(" ", "_").replace("-", "_")

def run_evolutionary_search() -> str:
    """
    Runs a simulation to find a superior genome.
    This is a simplified version of the federated learning experiment,
    focused on just finding one good genome to solve the problem.
    Returns the filepath to the winning genome.
    """
    print("\n--- 🔬 Starting Evolutionary Search for a Better Genome 🔬 ---")

    # We can reuse the setup from the federated learning experiment
    shared_event_bus = []
    alpha_sim, _ = setup_hives(shared_event_bus)
    operator = BeekeeperOperator()

    # Run the simulation long enough for a discovery
    for _ in range(11):
        operator.run_simulation_cycle(alpha_sim)
        if shared_event_bus:
            break

    if not shared_event_bus:
        print("  -> ❌ SEARCH FAILED: No superior genome was discovered in time.")
        return None

    # Extract the winning genome from the waggle dance event
    winning_dance = shared_event_bus[0]
    winning_genome = winning_dance.genome

    # For the genesis engine, we need a yaml file. Let's create one.
    genome_dict = {
        "name": "EvolvedOrderProcessor",
        "purpose": winning_genome.purpose,
        "primitive_type": winning_genome.primitive_type,
        "bonds": {
            "consumes": [{"command": "CreateNewOrder", "handler": "handle_creation_command"}],
            "produces": [{"event": "OrderCreated"}]
        },
        "nectar_production_rate": winning_genome.nectar_production_rate,
        "algorithm_complexity": "O(1)", # Assuming the best for the winner
        "error_handling_level": "robust",
        "traits": ["evolved", "caching"]
    }

    genome_path = "evolved_genome.yaml"
    with open(genome_path, 'w') as f:
        import yaml
        yaml.dump(genome_dict, f)

    print(f"  -> ✅ SEARCH COMPLETE: Superior genome discovered and saved to {genome_path}")
    return genome_path


def main():
    """
    Main entry point for the Age of Genesis Experiment.
    This demonstrates a full, autonomous, self-healing loop.
    """
    print("--- 🏛️ Welcome to the Age of Genesis 🏛️ ---")
    print("      A demonstration of a self-healing system.")

    operator = BeekeeperOperator(health_threshold=90.0)

    # 1. Monitor the service until its health becomes critical
    while not operator.run_aiops_cycle():
        import time
        time.sleep(0.1) # Add a small delay for dramatic effect

    # 2. Health is critical, trigger the evolutionary search
    winning_genome_path = run_evolutionary_search()

    if not winning_genome_path:
        print("\n--- ❌ EXPERIMENT FAILED: Could not evolve a solution. ---")
        return

    # 3. Use the Genesis Engine to build the new component
    print("\n--- 🛠️ Initiating Genesis Protocol 🛠️ ---")

    # Clean up old generated component if it exists
    component_name = to_snake_case("EvolvedOrderProcessor")
    component_path = pathlib.Path("hive/components") / component_name
    if component_path.exists():
        shutil.rmtree(component_path)

    # Use runpy to execute the CLI module safely
    sys.argv = [
        "genesis-engine/cli.py",
        "synthesize",
        "--genome",
        winning_genome_path
    ]
    runpy.run_module("genesis-engine.cli", run_name="__main__")

    # 4. Verification
    print("\n--- ✅ VERIFICATION ✅ ---")
    assert component_path.exists(), "The new component directory was not created."
    assert (component_path / "organism.py").exists(), "organism.py was not generated."
    assert (component_path / "contracts.py").exists(), "contracts.py was not generated."
    print("  -> SUCCESS: New, evolved component has been successfully synthesized.")

    print("\n--- 🏛️ Age of Genesis Experiment Complete 🏛️ ---")


if __name__ == "__main__":
    main()
