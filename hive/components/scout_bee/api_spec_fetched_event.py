from dataclasses import dataclass

@dataclass
class ApiSpecFetchedEvent:
    """
    An event indicating an API spec has been successfully fetched.
    (Currently a marker event, not carrying data).
    """
    pass
