from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from .organism import DigitalOrganism

import math

# Define weights for the fitness function. This allows for easy tuning.
FITNESS_WEIGHTS = {
    "production_rate": 0.8, # Genetic potential is still most important
    "nectar_level": 0.2,    # Current success is a good indicator
    "engrams": 0.1,         # Reward learning
}

class FitnessJudge:
    """
    Calculates the "fitness" of a digital organism, quantifying its success
    and suitability for replication. This is the core of natural selection.
    """

    def calculate_fitness(self, organism: "DigitalOrganism", weights: Dict[str, float] = None) -> float:
        """
        Calculates a fitness score (0-100) based on a weighted average of
        the organism's current state and genetic potential, modified by age.
        """
        if weights is None:
            weights = FITNESS_WEIGHTS

        # Normalize metrics to a common scale (e.g., 0-1) before applying weights.
        norm_prod_rate = min(organism.metabolism.nectar_production_rate / 50.0, 1.0)
        norm_nectar = min(organism.metabolism.nectar_level / 1000.0, 1.0)
        norm_engrams = min(len(organism.epigenome.engrams) / 10.0, 1.0)

        # Calculate a base score on production and current state
        base_score = (
            norm_prod_rate * weights.get("production_rate", 0) +
            norm_nectar * weights.get("nectar_level", 0) +
            norm_engrams * weights.get("engrams", 0)
        )

        # Apply an age factor. Wisdom of the elders.
        age_factor = 1 + (math.log(max(1, organism.metabolism.age)) * weights.get("age", 0))

        # Final score is base score modified by age
        final_score = max(0, min(100, base_score * 100 * (1 + age_factor)))

        return final_score
