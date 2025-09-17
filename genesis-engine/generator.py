import os
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any
from .parser import GenerationContext

import re

# Utility to convert strings to various cases
def snake_to_pascal(snake_case_string: str) -> str:
    """Converts snake_case or kebab-case to PascalCase."""
    return snake_case_string.replace("-", "_").replace("_", " ").title().replace(" ", "")

def to_snake_case(name: str) -> str:
    """Converts a name to snake_case."""
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower().replace(" ", "_").replace("-", "_")

class CodeGenerator:
    """
    Generates Python code from a parsed genome.
    """

    def __init__(self, template_dir: str = "genesis-engine/templates/organism"):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        # Add custom filters to the Jinja2 environment
        self.env.filters['pascal_case'] = snake_to_pascal
        self.env.filters['snake_case'] = to_snake_case

    def _create_template_data(self, context: GenerationContext) -> Dict[str, Any]:
        """Creates the dictionary expected by the Jinja2 templates."""
        return {
            "name": context.name,
            "purpose": context.genome.purpose,
            "primitive_type": context.genome.primitive_type.name,
            "bonds": context.bonds_map,
            "genetic_traits": {
                "nectar_production_rate": context.genome.nectar_production_rate
            }
        }

    def generate_organism_file(self, context: GenerationContext) -> str:
        """Generates the content for the main organism.py file."""
        template = self.env.get_template("organism.py.j2")
        template_data = self._create_template_data(context)
        return template.render(genome=template_data)

    def generate_contracts_file(self, context: GenerationContext) -> str:
        """Generates the content for the events.py/commands.py file."""
        template = self.env.get_template("contracts.py.j2")
        template_data = self._create_template_data(context)
        return template.render(genome=template_data)

    def generate_test_file(self, context: GenerationContext) -> str:
        """Generates the content for the test scaffold."""
        template = self.env.get_template("test_organism.py.j2")
        template_data = self._create_template_data(context)
        return template.render(genome=template_data)
