from dataclasses import dataclass
from typing import Dict, Any

# Forward declaration for type hinting
class DigitalOrganism:
    pass


@dataclass
class EthicalGovernor:
    """
    Enforces the Hive's Constitution to prevent harmful or uncontrolled evolution.
    This is the primary safety mechanism for the Hive and its simulations.
    """

    # Hard-coded constraints for safety
    max_replicas: int = 100
    max_age: int = 10000  # Ticks
    max_nectar_consumption_per_tick: int = 50
    min_nectar_level_for_replication: int = 500

    def check_action(
        self,
        organism: "DigitalOrganism",
        action_name: str,
        params: Dict[str, Any] = None,
    ) -> bool:
        """
        Checks if a proposed action is ethical and within safe limits.
        Returns True if the action is allowed, False otherwise.
        """
        if params is None:
            params = {}

        if action_name == "replicate":
            # Check if organism is healthy enough to replicate
            if organism.metabolism.nectar_level < self.min_nectar_level_for_replication:
                print(f"ETHICS VIOLATION: {organism.id} cannot replicate. Nectar too low.")
                return False
            # We would need a way to check total replicas of this type.
            # This check will be enhanced in the simulator context.
            return True

        if action_name == "consume_nectar":
            amount = params.get("amount", 0)
            if amount > self.max_nectar_consumption_per_tick:
                print(f"ETHICS VIOLATION: {organism.id} tried to consume too much nectar.")
                return False

        if organism.metabolism.age > self.max_age:
            print(f"ETHICS VIOLATION: {organism.id} has exceeded max age.")
            # This should trigger apoptosis, not just block actions.
            return False

        return True
