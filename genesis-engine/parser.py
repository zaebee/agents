import yaml
from typing import Dict, Any

class GenomeValidationError(Exception):
    """Custom exception for genome validation errors."""
    pass

def parse_genome(file_path: str) -> Dict[str, Any]:
    """
    Parses and validates a genome.yaml file.

    Args:
        file_path: The path to the genome.yaml file.

    Returns:
        A dictionary containing the validated genome data.

    Raises:
        FileNotFoundError: If the file does not exist.
        GenomeValidationError: If the genome file is missing required keys.
    """
    print(f"  -> Parsing genome from {file_path}...")
    try:
        with open(file_path, 'r') as f:
            genome_data = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Genome file not found at: {file_path}")
    except yaml.YAMLError as e:
        raise GenomeValidationError(f"Error parsing YAML file: {e}")

    # Validation
    required_keys = ['name', 'purpose', 'primitive_type', 'bonds']
    for key in required_keys:
        if key not in genome_data:
            raise GenomeValidationError(f"Missing required key in genome.yaml: '{key}'")

    if 'consumes' not in genome_data['bonds'] and 'produces' not in genome_data['bonds']:
        raise GenomeValidationError("The 'bonds' section must contain at least one of 'consumes' or 'produces'.")

    print("  -> Genome validation successful.")
    return genome_data
