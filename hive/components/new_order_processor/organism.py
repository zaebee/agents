from dna_core.royal_jelly.organism import DigitalOrganism, Genome
from dna_core.royal_jelly.periodic_table import ElementSymbol
from .contracts import (
    # Import contracts generated from the genome
    CreateneworderCommand,
    OrdercreatedEvent,OrderrejectedEvent,
)

class Neworderprocessor(DigitalOrganism):
    """
    Handles the initial creation and validation of a customer order.

    This organism was synthesized by the Genesis Engine.
    """

    def __init__(self, generation: int = 1):
        genome = Genome(
            primitive_type=ElementSymbol.A,
            bonds_template=("CreateNewOrder","OrderCreated","OrderRejected",),
            valency=(1, 2),
            purpose="Handles the initial creation and validation of a customer order.",
            nectar_production_rate=1
        )
        super().__init__(genome=genome, generation=generation)

    # --- Command Handlers ---

    def handle_creation_command(self, command: CreateneworderCommand):
        """Handler for the CreateneworderCommand."""
        print(f"  ->  handling CreateneworderCommand...")
        # TODO: Implement business logic for this command.
        # This handler should consume nectar and produce one of the
        # events defined in the 'produces' section of the genome.

        # Example:
        # self.consume_nectar(10)
        # return OrdercreatedEvent(...)
        pass


    # Override the abstract main_function to route commands
    def main_function(self, command):
        """Routes incoming commands to the appropriate handler."""

        if isinstance(command, CreateneworderCommand):
            return self.handle_creation_command(command)

        raise TypeError(f"Unknown command type received: {type(command)}")