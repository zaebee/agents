# genesis_engine/src/generator.py

def generate_code_from_ast(ast: dict, templates: dict) -> dict:
    """
    Generates a dictionary of filename: content from an AST and templates.
    This is our "Code Generation Transformation" (T).
    """
    generated_files = {}

    for node_id, data in ast.items():
        # Each component gets a data class ('honey' payload)
        payload_template = templates.get('payload')
        if payload_template:
            data_class_filename = f"data_models/{data['data_class'].lower()}.py"
            data_class_code = payload_template.format(
                class_name=data['data_class'],
                primary_key=data['primary_key']
            )
            generated_files[data_class_filename] = data_class_code

        # Generate the main component file based on the node type
        if node_id == 'C':
            template = templates.get('C')
            filename = "connector.py"
        elif node_id == 'A':
            template = templates.get('A')
            filename = "aggregate.py"
        elif node_id == 'G':
            template = templates.get('G')
            filename = "event.py"
        else:
            continue

        if template:
            code = template.format(**data)
            generated_files[filename] = code

    return generated_files
