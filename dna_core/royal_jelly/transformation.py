from abc import ABC

class Transformation(ABC):
    """
    Base class for a Transformation.

    In the Hive Architecture, a Transformation is a stateless service that
    contains domain logic that doesn't naturally fit within an Aggregate.
    It can be used by Aggregates or Connectors.

    Think of it as a collection of pure functions for a specific domain concept
    (e.g., a PricingCalculator).
    """
    pass
