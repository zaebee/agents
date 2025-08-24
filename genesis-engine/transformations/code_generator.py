# The "Enzyme" of our Genesis Engine - The Code Generation Transformation

import os
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field

# This would be a real, importable class from our dna-core library
from ..aggregates.compiler_aggregate import ComponentHatchingInitiated

@dataclass
class CodeGenerated:
    """An event indicating that the code for a file has been generated."""
    component_path: str
    file_name: str
    file_content: str
    event_type: str = field(default="CodeGenerated", init=False)

class CodeGenerationTransformation:
    """
    This transformation listens for hatching events and generates the
    code for the new component's files from tRNA templates.
    """
    def __init__(self, template_dir: str):
        self._template_dir = template_dir
        print("  - CodeGenerationTransformation initialized.")

    def process(self, event: ComponentHatchingInitiated) -> List[CodeGenerated]:
        """
        Reads the tRNA templates and generates the code for each file.
        """
        print(f"  - CodeGenerator processing event '{event.event_type}'...")
        generated_files: List[CodeGenerated] = []

        for template_name in event.templates:
            template_path = os.path.join(self._template_dir, template_name)

            try:
                with open(template_path, 'r') as f:
                    template_content = f.read()

                # This is where the "honey" would be injected in a real system.
                # We would replace placeholders like {class_name} here.
                # For now, we just use the raw template content.
                final_content = template_content.replace("{class_name}", event.component_name.capitalize())

                # The filename should be based on the component name, not the template name.
                # e.g., A.py.tpl -> create_order_aggregate.py
                # This logic is simplified for now.
                output_filename = template_name.replace('.tpl', '')

                generated_files.append(
                    CodeGenerated(
                        component_path=event.component_path,
                        file_name=output_filename,
                        file_content=final_content
                    )
                )
                print(f"    - Generated code from template: {template_name}")

            except FileNotFoundError:
                print(f"Warning: Template not found at {template_path}. Skipping.")

        return generated_files
