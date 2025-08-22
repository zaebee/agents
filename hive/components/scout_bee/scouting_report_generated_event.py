from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class ScoutingReportGeneratedEvent:
    """
    An event produced when a scouting session is complete.
    """
    aggregate_id: str
    report: Dict[str, Any] = field(default_factory=dict)
