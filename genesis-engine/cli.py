#!/usr/bin/env python3

import argparse
import sys
import os

# Add project root to path before other imports
# This ensures that dna_core and other modules can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dna_core.royal_jelly import PeriodicTable

# --- Command Handlers ---

def handle_table_command(args):
    """Display the Hive's Periodic Table."""
    print("Summoning the Periodic Table of Primitives...")
    PeriodicTable.print_table()

def handle_compat_command(args):
    """Check if two primitives can bond."""
    print(f"🔬 Compatibility Check: {args.element1} + {args.element2}")

    # This is a simplified check based on the new SDK
    # A real implementation might be more complex
    is_compatible = PeriodicTable.predict_compatibility(args.element1, args.element2)
    toxicity1 = PeriodicTable.check_toxicity(args.element1)
    toxicity2 = PeriodicTable.check_toxicity(args.element2)

    print(f"   ✅ Compatible: {'Yes' if is_compatible else 'No'}")
    print(f"   ⚠️ Toxicity: {args.element1} ({toxicity1}), {args.element2} ({toxicity2})")

    if "high" in [toxicity1, toxicity2]:
        print("   💀 Warning: High toxicity detected! This bond is unstable and not recommended.")

def handle_unimplemented(args):
    """Handler for commands that are defined in the Grimoire but not yet implemented."""
    print(f"Command '{args.command}' is defined in the Grimoire but not yet implemented.")
    print("The Hive's magic is still growing. Check back later!")

import pathlib
import shutil
import re
from .parser import parse_genome, GenomeValidationError
from .generator import CodeGenerator

def to_snake_case(name: str) -> str:
    """Converts a name to snake_case."""
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower().replace(" ", "_").replace("-", "_")

def handle_synthesize_command(args):
    """Handler for the new genome-based synthesis command."""
    try:
        print(f"🧬 Synthesizing new organism from genome: {args.genome}")

        # 1. Parse and validate the genome
        genome_data = parse_genome(args.genome)

        # 2. Prepare paths and directories
        component_name = genome_data['name']
        component_dir_name = to_snake_case(component_name)
        base_path = pathlib.Path("hive/components") / component_dir_name

        if base_path.exists():
            print(f"❌ Error: Component '{component_name}' already exists at {base_path}.")
            return

        base_path.mkdir(parents=True)
        (base_path / "tests").mkdir()
        print(f"  -> Created directory structure at {base_path}")

        # 3. Generate code
        generator = CodeGenerator()
        organism_code = generator.generate_organism_file(genome_data)
        contracts_code = generator.generate_contracts_file(genome_data)
        test_code = generator.generate_test_file(genome_data)

        # 4. Write generated files
        with open(base_path / "organism.py", "w") as f:
            f.write(organism_code)
        print(f"  -> Wrote organism.py")

        with open(base_path / "contracts.py", "w") as f:
            f.write(contracts_code)
        print(f"  -> Wrote contracts.py")

        with open(base_path / "tests/__init__.py", "w") as f:
            f.write("") # Make tests a package

        with open(base_path / "tests/test_organism.py", "w") as f:
            f.write(test_code)
        print(f"  -> Wrote tests/test_organism.py")

        # 5. Copy the genome file
        genome_file = pathlib.Path(args.genome)
        shutil.copy(genome_file, base_path / genome_file.name)
        print(f"  -> Copied genome.yaml to component directory.")

        print("\n✅ Synthesis complete! A new bee is ready to be taught its purpose.")

    except (FileNotFoundError, GenomeValidationError) as e:
        print(f"❌ Error: {e}")

# --- Main CLI Setup ---

def main():
    """Main entry point for the Alchemist's CLI."""
    parser = argparse.ArgumentParser(
        description="📜 The Beekeeper’s Grimoire: A CLI for tending to the Hive.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available spells")

    # --- `table` command ---
    table_parser = subparsers.add_parser("table", help="Display the Hive's Periodic Table of Primitives.")
    table_parser.set_defaults(func=handle_table_command)

    # --- `compat` command ---
    compat_parser = subparsers.add_parser("compat", help="Check the chemical compatibility of two primitives.")
    compat_parser.add_argument("element1", help="The name of the first primitive (e.g., OrderAggregate)")
    compat_parser.add_argument("element2", help="The name of the second primitive (e.g., OrderPlacedEvent)")
    compat_parser.set_defaults(func=handle_compat_command)

    # --- `synthesize` command ---
    synthesize_parser = subparsers.add_parser("synthesize", help="Create a new organism from a genome.yaml file.")
    synthesize_parser.add_argument("--genome", required=True, help="Path to the genome.yaml file.")
    synthesize_parser.set_defaults(func=handle_synthesize_command)

    # --- Placeholder commands from the Grimoire ---
    # This makes the CLI aware of future commands and provides a helpful message.
    placeholder_commands = [
        "inspect", "cull", "observe", "advise", "feed",
        "plant", "harvest", "archive", "cure", "refine", "analyze",
        "list", "health", "history", "plan"
    ]
    for command in placeholder_commands:
        placeholder_parser = subparsers.add_parser(command, help=f"(Not yet implemented) See Grimoire for details on '{command}'.")
        placeholder_parser.set_defaults(func=handle_unimplemented)

    args = parser.parse_args()

    # Execute the function associated with the chosen sub-command
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
