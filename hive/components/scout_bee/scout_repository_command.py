from dataclasses import dataclass
from typing import Optional

@dataclass
class ScoutRepositoryCommand:
    """
    A command to initiate the scouting of a GitHub repository.
    """
    url: str
    github_token: Optional[str] = None
