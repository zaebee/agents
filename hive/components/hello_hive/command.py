from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class HelloHiveCommand:
    """
    A command to create a new hello-hive.
    """
    payload: Dict[str, Any]
