# genesis_engine/src/template_loader.py
import os

def load_templates(template_dir: str = "tRNA") -> dict:
    """
    Loads code templates from the tRNA/ directory.
    This is part of the Ribosome's function, preparing the tRNA.
    """
    templates = {}
    if not os.path.exists(template_dir):
        raise FileNotFoundError(f"Template directory not found: {template_dir}")

    for filename in os.listdir(template_dir):
        if filename.endswith(".tpl"):
            # Use the part of the filename before .py.tpl as the key
            key = filename.split('.')[0]
            with open(os.path.join(template_dir, filename), 'r') as f:
                templates[key] = f.read()

    if not templates:
        raise ValueError(f"No .tpl files found in template directory: {template_dir}")

    return templates
