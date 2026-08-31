import os
from typing import List
from dna_core.royal_jelly import Transform

class RepositoryTransformer(Transform[str, List[str]]):
    """
    A transformation that walks a directory and returns paths to source files.
    Element: T (Transform)
    """

    def execute(self, repo_path: str) -> List[str]:
        """
        Walks the directory tree of a cloned repository and returns file paths.

        Args:
            repo_path: The local path to the cloned repository.

        Returns:
            A list of full paths to each source file ('.py' or '.ts') found.
        """
        print("Analyzing the hive's structure...")
        source_files = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(('.py', '.ts')):
                    filepath = os.path.join(root, file)
                    source_files.append(filepath)
        return source_files
