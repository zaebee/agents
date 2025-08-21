# The CLI Connector (Primary/Driving Adapter)

# We need the definition of the command to create it.
from ..aggregates.compiler_aggregate import HatchCommand

class CliConnector:
    """
    Translates user input from the command line into a formal command
    and passes it to the command handler (our application service).
    """
    def __init__(self, command_handler):
        self.command_handler = command_handler

    def hatch(self, codon_type: str, component_name: str):
        """
        The entry point for the 'hatch' command from the CLI.
        """
        print(f"CliConnector: Received hatch request for '{component_name}' with codon '{codon_type}'.")
        # 1. Translate the raw CLI input into a formal Command object.
        command = HatchCommand(codon_type=codon_type, component_name=component_name)

        # 2. Pass the command to the application's command handler.
        self.command_handler(command)

    def spin(self, component_name: str):
        """
        Placeholder for the 'spin' command.
        """
        print(f"Spin command for '{component_name}' is under construction.")
