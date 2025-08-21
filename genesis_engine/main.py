# genesis_engine/main.py
# This script is the "Application Layer" of our Compiler Hive.
# It composes the primitives from the `src/` directory to execute a compilation.

import argparse
import os
import sys

# Add the src directory to the Python path to allow for clean imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from parser import parse_mermaid_diagram
from template_loader import load_templates
from generator import generate_code_from_ast
from domain import StartCompilation, CompilationFinished

def main():
    """The main entrypoint for the Genesis Engine."""

    # This acts as our CLI Connector (C), parsing the user's intent.
    parser = argparse.ArgumentParser(
        description="The Genesis Engine - A Mermaid-driven code generator.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("source_file", help="Path to the source markdown file with the Mermaid diagram.")
    parser.add_argument("output_dir", help="Directory to write the generated code files to.")
    args = parser.parse_args()

    # The command created by the Connector
    command = StartCompilation(source_path=args.source_file, output_dir=args.output_dir)

    print(f"🔥 Starting The Genesis Engine...")
    print(f"   - Command Received: Compile {command.source_path}")

    # The following block acts as our "CompilerAggregate" (A) handling the command.
    try:
        # 1. Load tRNA templates (a supporting domain service)
        templates = load_templates()
        print(f"   - Loaded {len(templates)} tRNA templates.")

        # 2. Read source file
        with open(command.source_path, 'r') as f:
            content = f.read()

        # 3. Parse diagram to create an Abstract Syntax Tree (AST)
        ast = parse_mermaid_diagram(content)
        print(f"   - Parsed {len(ast)} nodes from diagram's genetic code.")

        # 4. Use a Transformation (T) to generate code
        generated_files = generate_code_from_ast(ast, templates)
        print(f"   - Generated {len(generated_files)} code files in memory.")

        # 5. Write files to disk (conceptually, a "FileWriterConnector")
        for filename, file_content in generated_files.items():
            filepath = os.path.join(command.output_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(file_content)
            print(f"     - Hatched file: {filepath}")

        # 6. Emit a final Genesis Event (G)
        final_event = CompilationFinished(
            output_dir=command.output_dir,
            num_files_generated=len(generated_files)
        )
        print(f"✅ {final_event}")

    except (FileNotFoundError, ValueError) as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
