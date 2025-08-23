import uuid
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
            nectar_production_rate=5
        )
        super().__init__(genome=genome, generation=generation)

    # --- Command Handlers ---

    def handle_creation_command(self, command: CreateneworderCommand):
        """Handler for the CreateneworderCommand."""
        print(f"  -> {self.id} handling CreateneworderCommand for customer {command.customer_id}...")

        self.consume_nectar(20) # Cost of processing an order

        if not command.items:
            print(f"  -> Order rejected for customer {command.customer_id}: No items provided.")
            return OrderrejectedEvent(
                customer_id=command.customer_id,
                reason="Order must contain at least one item.",
                correlation_id=command.correlation_id
            )

        order_id = f"order-{uuid.uuid4()}"
        print(f"  -> Order created for customer {command.customer_id} with new ID {order_id}.")
        return OrdercreatedEvent(
            order_id=order_id,
            customer_id=command.customer_id,
            items=command.items,
            correlation_id=command.correlation_id
        )


    # Override the abstract main_function to route commands
    def main_function(self, command):
        """Routes incoming commands to the appropriate handler."""

        if isinstance(command, CreateneworderCommand):
            return self.handle_creation_command(command)

        raise TypeError(f"Unknown command type received: {type(command)}")