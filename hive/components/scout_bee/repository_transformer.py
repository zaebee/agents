import os
from typing import Generator
from dna_core.royal_jelly import Transformation

class RepositoryTransformer(Transformation):
    """
    A transformation that walks a directory and yields paths to source files.
    """

    def transform(self, repo_path: str) -> Generator[str, None, None]:
        """
        Walks the directory tree of a cloned repository and yields file paths.

        Args:
            repo_path: The local path to the cloned repository.

        Yields:
            The full path to each source file ('.py' or '.ts') found.
        """
        print("Analyzing the hive's structure...")
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(('.py', '.ts')):
                    filepath = os.path.join(root, file)
                    yield filepath
