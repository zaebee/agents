from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class ${ClassName}Command:
    """
    A command to create a new ${ComponentName}.
    """
    payload: Dict[str, Any]
