from abc import ABC

class Connector(ABC):
    """
    Base class for a Connector.

    Connectors are the bridge between the domain core (Aggregates, Events) and
    the outside world (e.g., REST APIs, databases, message queues).

    They come in two flavors:
    1. Primary/Driving Connectors: Adapt external requests into calls to the domain
       (e.g., a Flask route handler calling an application service).
    2. Secondary/Driven Connectors: Adapt domain needs into calls to external systems
       (e.g., a repository implementation that talks to a database).
    """
    pass
