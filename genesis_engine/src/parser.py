# genesis_engine/src/parser.py
import re

def parse_mermaid_diagram(content: str) -> dict:
    """
    Parses a Mermaid diagram to extract nodes and their style contracts.
    This function represents a core part of our "Transformation" primitive.
    """

    # Regex to find nodes like "C[WebConnector]"
    node_regex = re.compile(r'(\w+)\[(.*?)\]')
    # Regex to find styles like "style C fill:CreateOrderCommand,stroke:user_id"
    style_regex = re.compile(r'style\s+(\w+)\s+fill:(\w+),stroke:(\w+)')

    # Find the mermaid block within the markdown content
    mermaid_content_match = re.search(r'```mermaid(.*?)```', content, re.DOTALL)
    if not mermaid_content_match:
        raise ValueError("No mermaid diagram found in the source file.")

    mermaid_content = mermaid_content_match.group(1)

    # Parse nodes and their class names
    nodes = {match.groups()[0]: {'class_name': match.groups()[1]} for match in node_regex.finditer(mermaid_content)}

    # Parse style information and add it to the nodes dictionary
    for match in style_regex.finditer(mermaid_content):
        node_id, data_class, primary_key = match.groups()
        if node_id in nodes:
            nodes[node_id]['data_class'] = data_class
            nodes[node_id]['primary_key'] = primary_key
            nodes[node_id]['data_class_lower'] = data_class.lower()

    if not nodes:
        raise ValueError("Could not parse any valid nodes from the Mermaid diagram.")

    return nodes
