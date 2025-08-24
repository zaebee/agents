# The "Output Sense" of our Genesis Engine - The File Writer Connector

import os
from typing import List

# This would be a real, importable class
from ..transformations.code_generator import CodeGenerated

class FileWriterConnector:
    """
    This connector's job is to take generated code (from a CodeGenerated event)
    and perform the infrastructure task of writing it to the file system.
    """
    def __init__(self):
        print("  - FileWriterConnector initialized.")

    def handle(self, events: List[CodeGenerated]):
        """
        Receives a list of CodeGenerated events and writes each to disk.
        """
        print("  - FileWriterConnector handling generated code...")
        if not events:
            print("    - No code to write.")
            return

        component_path = events[0].component_path

        # 1. Ensure the target directory exists
        if not os.path.exists(component_path):
            print(f"    - Creating directory: {component_path}")
            os.makedirs(component_path)

        # 2. Write each file
        for event in events:
            file_path = os.path.join(event.component_path, event.file_name)
            print(f"    - Writing file: {file_path}")
            with open(file_path, 'w') as f:
                f.write(event.file_content)

        print(f"\nSuccess! New codon hatched at: {component_path}")
        print("Next steps: 'spin cocoon' to add tests.")
