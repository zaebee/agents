import re
from dna_core.royal_jelly import Transformation

class SourceFileTransformer(Transformation):
    """
    A transformation for parsing individual source files (.py, .ts)
    to find class definitions that inherit from Royal Jelly / ATCG primitives.
    """

    def transform(self, filepath: str) -> dict:
        """
        Analyzes a single source file and returns discovered components.

        Args:
            filepath: The path to the source file.

        Returns:
            A dictionary of discovered components, e.g.,
            {"aggregates": ["MyAggregate"], "connectors": [], "transformations": []}
        """
        if filepath.endswith('.py'):
            return self._analyze_py_file(filepath)
        elif filepath.endswith('.ts'):
            return self._analyze_ts_file(filepath)
        else:
            return {"aggregates": [], "transformations": [], "connectors": []}

    def _analyze_ts_file(self, filepath: str) -> dict:
        """Parses a TypeScript file with regex."""
        components = {"aggregates": [], "transformations": [], "connectors": []}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            pattern = r"class\s+([A-Za-z0-9_]+)\s+extends\s+([A-Za-z0-9_]+)"
            matches = re.findall(pattern, content)

            for class_name, base_class in matches:
                if base_class == 'Aggregate':
                    components["aggregates"].append(class_name)
                elif base_class == 'Connector':
                    components["connectors"].append(class_name)
                elif base_class == 'Transformation':
                    components["transformations"].append(class_name)
        except Exception:
            pass  # Ignore files that can't be read
        return components

    def _analyze_py_file(self, filepath: str) -> dict:
        """Parses a Python file with regex."""
        components = {"aggregates": [], "transformations": [], "connectors": []}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            pattern = r"class\s+([A-Za-z0-9_]+)\s*\(([A-Za-z0-9_]+)\):"
            matches = re.findall(pattern, content)

            for class_name, base_class in matches:
                if base_class == 'Aggregate':
                    components["aggregates"].append(class_name)
                elif base_class == 'Connector':
                    components["connectors"].append(class_name)
                elif base_class == 'Transformation':
                    components["transformations"].append(class_name)
        except Exception:
            pass  # Ignore files that can't be read
        return components
