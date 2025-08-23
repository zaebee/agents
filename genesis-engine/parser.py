import yaml
from dataclasses import dataclass
from typing import Dict, Any
from dna_core.royal_jelly.organism import Genome
from dna_core.royal_jelly.periodic_table import ElementSymbol

@dataclass
class GenerationContext:
    """A container for the Genome and other metadata needed for code generation."""
    genome: Genome
    name: str
    bonds_map: Dict[str, Any]

class GenomeValidationError(Exception):
    """Custom exception for genome validation errors."""
    pass

def parse_genome(file_path: str) -> GenerationContext:
    """
    Parses a genome.yaml file and constructs a GenerationContext object.
    """
    print(f"  -> Parsing genome from {file_path}...")
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Genome file not found at: {file_path}")
    except yaml.YAMLError as e:
        raise GenomeValidationError(f"Error parsing YAML file: {e}")

    # --- Validation ---
    required_keys = ['name', 'purpose', 'primitive_type', 'bonds']
    for key in required_keys:
        if key not in data:
            raise GenomeValidationError(f"Missing required key in genome.yaml: '{key}'")

    if 'consumes' not in data['bonds'] and 'produces' not in data['bonds']:
        raise GenomeValidationError("The 'bonds' section must contain at least one of 'consumes' or 'produces'.")

    # --- Transformation ---
    try:
        primitive_type = ElementSymbol[data['primitive_type']]

        consumes = data['bonds'].get('consumes', [])
        produces = data['bonds'].get('produces', [])

        valency = (len(consumes), len(produces))
        bonds_template = tuple(consumes + produces)

        # Extract optional fields with defaults
        nectar_rate = data.get('nectar_production_rate', 1)
        complexity = data.get('algorithm_complexity', 'O(n)')
        error_level = data.get('error_handling_level', 'basic')
        traits = tuple(data.get('traits', []))

        genome = Genome(
            primitive_type=primitive_type,
            purpose=data['purpose'],
            bonds_template=bonds_template,
            valency=valency,
            nectar_production_rate=nectar_rate,
            algorithm_complexity=complexity,
            error_handling_level=error_level,
            traits=traits
        )

        context = GenerationContext(
            genome=genome,
            name=data['name'],
            bonds_map=data['bonds']
        )

    except KeyError as e:
        raise GenomeValidationError(f"Invalid primitive_type in genome: {e}")
    except Exception as e:
        raise GenomeValidationError(f"An unexpected error occurred during genome construction: {e}")

    print("  -> Genome parsing and construction successful.")
    return context
