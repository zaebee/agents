from typing import Dict, List, TYPE_CHECKING, Any
import numpy as np

if TYPE_CHECKING:
    from .organism import DigitalOrganism

from dna_core.royal_jelly.fitness import FITNESS_WEIGHTS as DEFAULT_WEIGHTS

class HiveMind:
    """
    Represents the collective consciousness and strategic direction of the Hive.
    It observes the state of the entire colony and sets goals to guide evolution.
    """

    GOAL_WEIGHTS = {
        "DEFAULT": DEFAULT_WEIGHTS,
        "GROW_POPULATION": {
            "production_rate": 0.5,
            "nectar_level": 0.1,
            "age": -0.3,  # Heavily favor youth for rapid expansion
            "engrams": 0.1,
        },
        "HOARD_NECTAR": {
            "production_rate": 0.2,
            "nectar_level": 0.8, # Overwhelmingly reward nectar storage
            "age": 0.0,
            "engrams": 0.0,
        },
        "IMPROVE_LATENCY": {
            "production_rate": 0.6, # Favor strong bees that can be optimized
            "nectar_level": 0.1,
            "age": 0.0,
            "engrams": 0.3, # Reward bees that have learned optimizations
        }
    }

    def __init__(self):
        self.global_metrics: Dict[str, float] = {}
        self.production_state: Dict[str, Any] = {}
        self.goal: str = "DEFAULT"
        print("🧠 HiveMind has awakened.")

    def ingest_production_metrics(self, metrics: Dict[str, Any]):
        """Consumes and stores metrics from the production environment."""
        self.production_state = metrics
        # The mind can now react to real-world conditions
        for component in self.production_state.get("components", []):
            if component.get("metrics", {}).get("latency_ms_p95", 0) > 200.0:
                print(f"  🧠 MIND ALERT: High latency detected for {component['name']}. Setting goal to IMPROVE_LATENCY.")
                self.set_goal("IMPROVE_LATENCY")


    def observe(self, organisms: List["DigitalOrganism"]):
        """
        Observes the entire population of organisms and calculates global metrics.
        This is the Hive's sensory input.
        """
        if not organisms:
            self.global_metrics = {
                "population": 0,
                "average_fitness": 0,
                "average_age": 0,
                "total_nectar": 0,
                "average_nectar_production": 0,
            }
            return

        self.global_metrics["population"] = len(organisms)
        self.global_metrics["average_fitness"] = np.mean([o.fitness_score for o in organisms])
        self.global_metrics["average_age"] = np.mean([o.metabolism.age for o in organisms])
        self.global_metrics["total_nectar"] = np.sum([o.metabolism.nectar_level for o in organisms])
        self.global_metrics["average_nectar_production"] = np.mean(
            [o.genome.nectar_production_rate for o in organisms]
        )

        # Optional: Print the hive's thoughts
        # print(f"  [HiveMind Observation]: {self.global_metrics}")

    def set_goal(self, goal: str):
        """Sets the Hive's current strategic goal."""
        if goal in self.GOAL_WEIGHTS:
            self.goal = goal
            print(f"  🧠 New Hive Goal set: {goal}")
        else:
            print(f"  ⚠️ Unknown goal: {goal}. Maintaining current goal: {self.goal}")

    def get_fitness_weights(self) -> Dict[str, float]:
        """Returns the fitness weight profile for the current goal."""
        return self.GOAL_WEIGHTS.get(self.goal, DEFAULT_WEIGHTS)

    def __repr__(self):
        return f"<HiveMind goal={self.goal} population={self.global_metrics.get('population', 0)}>"
