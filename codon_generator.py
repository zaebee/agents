# codon_generator.py
# A proof-of-concept script to generate boilerplate code from a feature definition.
#
# Requires PyYAML. To install: pip install PyYAML
#
# Usage: python codon_generator.py feature.yml

import yaml
import sys
import os

def generate_aggregate_code(name):
    """Generates a placeholder class for an Aggregate."""
    return f"""
class {name}:
    \"\"\"Represents the {name} aggregate.
    It enforces business rules for its domain.
    \"\"\"
    def __init__(self, state):
        self._state = state

    def handle_command(self, command):
        print(f"Handling command in {name}...")
        # In a real implementation, this method would contain the core
        # business logic to validate the command and, if successful,
        # produce and return one or more domain events.
        print(f"  - Command: {{command}}")
        pass
"""

def generate_connector_code(codon_data):
    """Generates placeholder code for a Connector based on a codon."""
    if codon_data['type'] == 'ReactToEvent':
        event = codon_data['listens_to']
        return f"""
class {event}EventConnector:
    \"\"\"A listening connector that reacts to {event} events.
    It translates the event into a command for its local domain.
    \"\"\"
    def __init__(self, service):
        self._service = service # An application service

    def listen_for_event(self, event):
        if event.type == "{event}":
            print(f"Event {{event.type}} received by {{self.__class__.__name__}}!")
            # The connector calls an application service,
            # which in turn finds and calls the appropriate aggregate.
            self._service.process_{event.lower()}(event.payload)
"""
    elif codon_data['type'] == 'HandleCommand':
        command = codon_data['command_name']
        return f"""
class {command}CommandConnector:
    \"\"\"A driving connector that handles the {command} command.
    It translates an external request (e.g., HTTP) into a domain command.
    \"\"\"
    def __init__(self, service):
        self._service = service # An application service

    def handle_request(self, request):
        print(f"Request for {command} received by {{self.__class__.__name__}}!")
        self._service.execute_{command.lower()}(request.data)
"""
    return ""


def generate_code(feature_data):
    """Main function to generate code for the entire feature."""

    feature_name = feature_data.get('feature_name', 'UnnamedFeature')
    generated_code = [f"# --- Generated Code for Feature: {feature_name} ---"]
    generated_code.append(f"# Description: {feature_data.get('description', 'No description.')}")
    generated_code.append(f"# Author: {feature_data.get('author', 'Unknown')}\\n")
    generated_code.append("-" * 50)

    aggregates_to_generate = set()
    codons = feature_data.get('codons', [])

    for codon in codons:
        if 'calls_aggregate' in codon:
            aggregates_to_generate.add(codon['calls_aggregate'])

    if aggregates_to_generate:
        generated_code.append("\\n# 1. AGGREGATES (The 'A' in ATCG)")
        generated_code.append("# These classes hold the core business logic and state.")
        for agg in sorted(list(aggregates_to_generate)):
            generated_code.append(generate_aggregate_code(agg))

    if codons:
        generated_code.append("\\n# 2. CONNECTORS (The 'C' in ATCG)")
        generated_code.append("# These classes are the bridge to the outside world.")
        for codon in codons:
            generated_code.append(generate_connector_code(codon))

    generated_code.append("\\n" + "-" * 50)
    generated_code.append("# --- End of Generated Code ---")
    return "\\n".join(generated_code)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python codon_generator.py <path_to_feature.yml>")
        sys.exit(1)

    yaml_file_path = sys.argv[1]

    if not os.path.exists(yaml_file_path):
        print(f"Error: File not found at {yaml_file_path}")
        sys.exit(1)

    print(f"🧬 Generating code from definition: {yaml_file_path}\\n")

    with open(yaml_file_path, 'r') as f:
        try:
            feature_definition = yaml.safe_load(f)
            generated_code = generate_code(feature_definition)
            print(generated_code)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)
