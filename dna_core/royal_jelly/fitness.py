from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .organism import Genome, DigitalOrganism

class FitnessJudge:
    """
    Calculates the "fitness" of a digital organism based purely on its
    inherent genetic traits (its Genome), not its current runtime state.
    """

    @staticmethod
    def calculate_genome_fitness(genome: "Genome") -> float:
        """
        Calculates a fitness score (0-100) based on the static Genome.
        This represents the bee's genetic potential.
        """
        score = 0.0

        # Reward efficient algorithms
        if genome.algorithm_complexity == "O(1)":
            score += 40
        elif genome.algorithm_complexity == "O(log n)":
            score += 25

        # Reward robust error handling
        if genome.error_handling_level == "robust":
            score += 30

        # Reward beneficial traits
        if "caching" in genome.traits:
            score += 20
        if "parallelism" in genome.traits:
            score += 15

        # Reward high production potential, but cap it to prevent it from dominating
        score += min(genome.nectar_production_rate, 50) / 2.0 # Max 25 points from production

        return max(0.0, min(100.0, score))
