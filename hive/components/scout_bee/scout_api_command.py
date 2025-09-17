from dataclasses import dataclass

@dataclass
class ScoutApiCommand:
    """
    A command to initiate the scouting of an OpenAPI specification.
    """
    url: str
