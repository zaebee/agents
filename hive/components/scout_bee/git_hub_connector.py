import tempfile
import shutil
from git import Repo
from typing import Dict, Any
from dna_core.royal_jelly import Connector

class GitHubConnector(Connector[Dict[str, Any], str]):
    """
    A connector for cloning a remote GitHub repository.
    Element: C (Connector)
    """

    def process(self, input_data: Dict[str, Any]) -> str:
        """
        Clones a GitHub repository into a temporary directory.

        Args:
            input_data: A dict with 'url' and optional 'github_token'.

        Returns:
            The path to the temporary directory where the repo was cloned.
        """
        repo_url = input_data.get("url")
        github_token = input_data.get("github_token")

        if not repo_url:
            raise ValueError("'url' not provided in input_data for GitHubConnector")

        temp_dir = tempfile.mkdtemp()
        print(f"Scout Bee is cloning {repo_url} into a temporary directory...")

        try:
            if github_token:
                repo_url = repo_url.replace("https://", f"https://{github_token}@")

            Repo.clone_from(repo_url, temp_dir)
            print("Cloning complete.")
            return temp_dir
        except Exception as e:
            print(f"Error during repository cloning: {e}")
            shutil.rmtree(temp_dir)
            raise
