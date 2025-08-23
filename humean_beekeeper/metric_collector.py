import random
from typing import Dict, Any

class MetricCollector:
    """
    Simulates a monitoring agent that collects health metrics from a production service.
    In a real system, this would connect to an observability platform.
    """

    def __init__(self, initial_health: float = 100.0):
        self.service_health = initial_health
        print(f"📈 Metric Collector initialized. Initial service health: {self.service_health:.2f}%")

    def collect(self) -> Dict[str, Any]:
        """Returns the current health metrics of the service."""
        return {
            "service_name": "NewOrderProcessor",
            "health_percent": self.service_health,
            "error_rate": (100.0 - self.service_health) / 100.0,
            "latency_ms": 50 + (100 - self.service_health) * 5
        }

    def degrade_service(self, amount: float = 5.0):
        """Degrades the service health by a random amount up to the specified value."""
        degradation = random.uniform(0, amount)
        self.service_health = max(0.0, self.service_health - degradation)
        print(f"  📉 Service health degraded. Current health: {self.service_health:.2f}%")
