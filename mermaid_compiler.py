# mermaid_compiler.py
# The Genesis Engine: A PoC for generating code from a Mermaid diagram.
#
# Usage: python mermaid_compiler.py <input_markdown_file> <output_directory>

import sys
import os
import re

# --- TEMPLATE LOADER ---

def load_templates():
    """Loads code templates from the templates/ directory."""
    template_dir = "templates"
    templates = {}
    for filename in os.listdir(template_dir):
        if filename.endswith(".tpl"):
            # Use the part of the filename before .py.tpl as the key
            key = filename.split('.')[0]
            with open(os.path.join(template_dir, filename), 'r') as f:
                templates[key] = f.read()
    return templates

# --- PARSING LOGIC ---

def parse_mermaid_diagram(content):
    """Parses a Mermaid diagram to extract nodes and their style contracts."""

    node_regex = re.compile(r'(\w+)\[(.*?)\]')
    style_regex = re.compile(r'style\s+(\w+)\s+fill:(\w+),stroke:(\w+)')

    nodes = {match.groups()[0]: {'class_name': match.groups()[1]} for match in node_regex.finditer(content)}

    for match in style_regex.finditer(content):
        node_id, data_class, primary_key = match.groups()
        if node_id in nodes:
            nodes[node_id]['data_class'] = data_class
            nodes[node_id]['primary_key'] = primary_key
            nodes[node_id]['data_class_lower'] = data_class.lower()

    return nodes

# --- MAIN COMPILER LOGIC ---

def compile_source(input_file, output_dir, templates):
    """Reads a source file, parses it, and generates code using loaded templates."""

    print(f"🔥 Starting The Genesis Engine...")
    print(f"   - Reading source from: {input_file}")

    with open(input_file, 'r') as f:
        content = f.read()

    mermaid_content = re.search(r'```mermaid(.*?)```', content, re.DOTALL)
    if not mermaid_content:
        raise ValueError("No mermaid diagram found in the source file.")

    nodes = parse_mermaid_diagram(mermaid_content.group(1))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"   - Created output directory: {output_dir}")

    # Generate files based on the node type (C, A, G)
    for node_id, data in nodes.items():
        # Generate the data class for the component's state/payload
        data_class_filename = f"data_models/{data['data_class'].lower()}.py"
        data_class_code = templates['data_class'].format(class_name=data['data_class'], primary_key=data['primary_key'])

        os.makedirs(os.path.join(output_dir, "data_models"), exist_ok=True)
        with open(os.path.join(output_dir, data_class_filename), 'w') as f:
            f.write(data_class_code)
        print(f"     - Hatched data model: {data_class_filename}")

        if node_id == 'C':
            filename = "connector.py"
            code = templates['connector'].format(**data)
        elif node_id == 'A':
            filename = "aggregate.py"
            code = templates['aggregate'].format(**data)
        elif node_id == 'G':
            filename = "event.py"
            code = templates['event'].format(**data)
        else:
            continue

        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(code)
        print(f"     - Hatched component: {filename}")

    print("✅ Compilation complete. The Hive grows stronger!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python mermaid_compiler.py <input_markdown_file> <output_directory>")
        sys.exit(1)

    try:
        loaded_templates = load_templates()
        compile_source(sys.argv[1], sys.argv[2], loaded_templates)
    except FileNotFoundError:
        print("\nError: `templates` directory not found.")
        print("Please ensure the `templates` directory with .tpl files exists in the same directory as the script.")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)
