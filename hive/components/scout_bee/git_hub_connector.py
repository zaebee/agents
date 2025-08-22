import tempfile
import shutil
from git import Repo
from dna_core.royal_jelly import Connector

class GitHubConnector(Connector):
    """
    A connector for cloning a remote GitHub repository.
    """

    def clone(self, repo_url: str, github_token: str = None) -> str:
        """
        Clones a GitHub repository into a temporary directory.

        Args:
            repo_url: The URL of the repository to clone.
            github_token: An optional GitHub token for private repositories.

        Returns:
            The path to the temporary directory where the repo was cloned.
        """
        temp_dir = tempfile.mkdtemp()
        print(f"Scout Bee is cloning {repo_url} into a temporary directory...")

        try:
            # Handle authentication for private repos if token is provided
            if github_token:
                repo_url = repo_url.replace("https://", f"https://{github_token}@")

            Repo.clone_from(repo_url, temp_dir)
            print("Cloning complete.")
            return temp_dir
        except Exception as e:
            print(f"Error during repository cloning: {e}")
            shutil.rmtree(temp_dir) # Clean up on failure
            raise
