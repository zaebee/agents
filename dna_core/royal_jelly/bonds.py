from collections import defaultdict
from typing import Dict, Tuple

class PlasticBonds:
    """
    Manages the dynamic, weighted connections between organisms in the Hive.
    This represents the Hive's nervous system, where pathways strengthen
    and weaken with use.
    """

    def __init__(self, decay_rate: float = 0.01):
        """
        Initializes the bond manager.

        Args:
            decay_rate: The rate at which unused bonds weaken per tick.
        """
        self.bonds: Dict[Tuple[str, str], float] = defaultdict(float)
        self.decay_rate = decay_rate

    def record_interaction(self, source_id: str, target_id: str, strength: float = 1.0):
        """
        Strengthens the bond between two organisms after a successful interaction.
        """
        key = (source_id, target_id)
        self.bonds[key] += strength
        print(f"  -> Bond strengthened: {source_id} -> {target_id} (New Strength: {self.bonds[key]:.2f})")

    def decay_bonds(self):
        """
        Applies a decay factor to all bonds. This simulates the weakening
        of unused neural pathways and keeps the graph sparse.
        """
        for key in list(self.bonds.keys()):
            self.bonds[key] *= (1 - self.decay_rate)
            if self.bonds[key] < 0.1:  # Prune very weak bonds
                del self.bonds[key]
                print(f"  -> Bond pruned: {key[0]} -> {key[1]}")

    def get_bond_strength(self, source_id: str, target_id: str) -> float:
        """Returns the strength of a specific bond."""
        return self.bonds.get((source_id, target_id), 0.0)

    def __repr__(self):
        return f"<PlasticBonds with {len(self.bonds)} active bonds>"
