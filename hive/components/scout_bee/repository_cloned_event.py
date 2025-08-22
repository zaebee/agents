from dataclasses import dataclass

@dataclass
class RepositoryClonedEvent:
    """
    An event indicating a repository has been successfully cloned.
    (Currently a marker event, not carrying data).
    """
    pass
