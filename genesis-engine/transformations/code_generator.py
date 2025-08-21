from dataclasses import dataclass, field
import os
from jinja2 import Environment, FileSystemLoader
from typing import List

# --- Data Class for Events ---

@dataclass
class CodeGenerated:
    """Event indicating a file's content has been generated."""
    filepath: str
    content: str
    event_type: str = "CodeGenerated"

# --- Transformation ---

class CodeGenerationTransformation:
    """
    Takes a 'ComponentHatchingInitiated' event and transforms it into
    'CodeGenerated' events by rendering templates.
    """
    def __init__(self, template_dir: str):
        self.template_path = os.path.join("genesis-engine", template_dir)
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.template_path),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def process(self, hatching_event) -> List[CodeGenerated]:
        """
        Processes the hatching event and returns a list of CodeGenerated events.
        """
        component_name = hatching_event.component_name
        target_dir = hatching_event.component_path
        templates_to_render = hatching_event.templates

        generated_events = []
        print(f"  - CodeGenerator: Processing {len(templates_to_render)} templates for '{component_name}'.")

        for template_file in templates_to_render:
            try:
                template = self.jinja_env.get_template(template_file)
            except Exception as e:
                print(f"FATAL: Could not load template '{template_file}'. Error: {e}")
                continue # Skip this template

            # Prepare context for rendering. A real implementation would be more sophisticated.
            class_name_base = component_name.replace('-', ' ').title().replace(' ', '')
            context = {
                "component_name": component_name,
                "class_name": class_name_base,
                "data_class": f"{class_name_base}Data",
                "data_class_lower": component_name.replace('-', '_'),
                "primary_key": "id",
                "command_purpose": "do something amazing",
                "query_purpose": "get something valuable",
                "dto_purpose": "some valuable data"
            }

            content = template.render(context)

            # The output filename is derived from the template name. This is a simple heuristic.
            # e.g., 'chronicler/quest.yaml.j2' -> 'quest.yaml'
            # e.g., 'C.py.tpl' -> 'connector.py'

            # A simple mapping for better filenames
            filename_map = {
                "A.py.tpl": "aggregate.py",
                "C.py.tpl": "connector.py",
                "G.py.tpl": "event.py",
                "T.py.tpl": "transformer.py",
                "command.py.tpl": "command.py",
                "query.py.tpl": "query.py",
                "dto.py.tpl": "dto.py",
                "immune.py.tpl": "immune_aggregate.py",
                "quest.yaml.j2": "quest.yaml"
            }

            base_template_name = os.path.basename(template_file)
            output_filename = filename_map.get(base_template_name, base_template_name.replace('.j2', '').replace('.tpl', ''))

            filepath = os.path.join(target_dir, output_filename)

            generated_events.append(CodeGenerated(filepath=filepath, content=content))
            print(f"    - Generated code for {filepath}")

        return generated_events
