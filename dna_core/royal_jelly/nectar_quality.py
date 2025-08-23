from typing import List, Dict, Any

class NectarQuality:
    """
    Calculates the 'quality' of work done by an organism by assigning
    value to the events it produces.
    """

    # The economic value of different events. This can be tuned.
    EVENT_VALUES = {
        "OrderCreatedEvent": 10,
        "OrderRejectedEvent": 2, # Still valuable information
        "FraudDetectedEvent": 50, # High value
        "PaymentProcessedEvent": 5,
        "LogEvent": 0.1, # Low value
        "Default": 1, # Default value for unknown events
    }

    @classmethod
    def calculate_quality(cls, events: List[Any]) -> float:
        """
        Calculates the average nectar quality for a list of processed events.

        Args:
            events: A list of event objects. Assumes event objects have a `__class__.__name__`

        Returns:
            The average value per event.
        """
        if not events:
            return 0.0

        total_value = sum(
            cls.EVENT_VALUES.get(event.__class__.__name__, cls.EVENT_VALUES["Default"])
            for event in events
        )

        return total_value / len(events)
