# The "Input Sense" of our Genesis Engine - The CLI Connector

from typing import Callable

# This would be a real, importable class
try:
    from ..aggregates.compiler_aggregate import HatchCommand
except ImportError:
    from aggregates.compiler_aggregate import HatchCommand


class CliConnector:
    """
    This connector's job is to translate user input from the command line
    into domain Commands for the aggregate to handle.
    """

    def __init__(self, command_handler: Callable):
        self._command_handler = command_handler
        print("  - CliConnector initialized.")

    def hatch(self, codon_type: str, component_name: str):
        """Translates a CLI call into a HatchCommand."""
        print(f"\n> CLI Connector received 'hatch {codon_type}' for '{component_name}'")

        # 1. Translate to command
        command = HatchCommand(codon_type=codon_type, component_name=component_name)

        # 2. Pass to handler (in our case, the aggregate)
        self._command_handler(command)

    def spin(self, component_name: str):
        """A placeholder for the spin command translation."""
        print(f"\n> CLI Connector received 'spin cocoon' for '{component_name}'")
        print("  - (Spin command logic is under construction in this new architecture)")
