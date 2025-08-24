"""
Enhanced HelloHive Aggregate with Sacred Codon Implementation

This demonstrates how to use the Sacred Codon patterns with Jules' foundational
PollenEnvelope and Protobuf architecture, creating a bridge between the
fairy tale architecture and the technical implementation.
"""

import uuid
from typing import List, Dict, Any
from datetime import datetime, timezone
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp
from dna_core.pollen_protocol_pb2 import PollenEnvelope
from dna_core.royal_jelly import (
    SacredAggregate,
    SacredCommand,
    SacredCodonType,
    create_sacred_command,
)


class HelloHiveSacredAggregate(SacredAggregate):
    """
    Enhanced HelloHive Aggregate implementing Sacred Codon patterns.

    This aggregate demonstrates:
    - Handle Command Codon (C→A→G) for greeting creation
    - Query Data Codon (C→T→C) for greeting retrieval
    - React to Event Codon (G→C→A→G) for greeting responses
    - Immune Response Codon (G→C→A→C) for error handling

    Sacred Pattern: This follows the Beekeeper's wisdom that every component
    must have a clear purpose and follow the genetic architecture patterns.
    """

    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
        self.greeting_count = 0
        self.greetings_sent = []
        self.status = "initialized"
        self.last_greeting = None

    def create_greeting(self, greeting_data: Dict[str, Any]) -> List[PollenEnvelope]:
        """
        Sacred Codon: Handle Command (C→A→G) - Create a new greeting

        This demonstrates the fundamental pattern for changing state:
        1. External request comes through connector (C)
        2. Aggregate processes business logic (A)
        3. Genesis Event records the change (G)
        """
        # Create Sacred Command following C→A→G pattern
        command = create_sacred_command(
            command_type="create_greeting",
            payload=greeting_data,
            codon_type=SacredCodonType.HANDLE_COMMAND,
            source="hello_hive_connector",
        )

        # Execute the Sacred Codon
        return self.execute_handle_command_codon(command)

    def get_greeting_stats(self) -> Dict[str, Any]:
        """
        Sacred Codon: Query Data (C→T→C) - Retrieve greeting statistics

        This demonstrates the pure query pattern with no state changes:
        1. Query request comes through connector (C)
        2. Transformation processes the data (T)
        3. Result returns through connector (C)
        """
        # Create Sacred Query Command
        query_command = create_sacred_command(
            command_type="get_greeting_stats",
            payload={"aggregate_id": self.id},
            codon_type=SacredCodonType.QUERY_DATA,
            source="hello_hive_query_connector",
        )

        # Execute the Sacred Codon
        return self.execute_query_data_codon(query_command)

    def respond_to_greeting(
        self, greeting_event: PollenEnvelope
    ) -> List[PollenEnvelope]:
        """
        Sacred Codon: React to Event (G→C→A→G) - Respond to another greeting

        This demonstrates event-driven choreography:
        1. Genesis Event arrives from another component (G)
        2. Connector translates to internal command (C)
        3. Aggregate processes the reaction (A)
        4. Genesis Event records the response (G)
        """
        return self.execute_react_to_event_codon(greeting_event)

    def handle_greeting_error(
        self, error_event: PollenEnvelope
    ) -> List[PollenEnvelope]:
        """
        Sacred Codon: Immune Response (G→C→A→C) - Handle greeting errors

        This demonstrates the self-healing pattern:
        1. Genesis Event signals an error (G)
        2. Connector translates to immune command (C)
        3. Aggregate determines corrective action (A)
        4. Connector executes correction (C)
        """
        return self.execute_immune_response_codon(error_event)

    # Implementation of Sacred Codon abstract methods

    def _execute_command_logic(self, command: SacredCommand) -> List[PollenEnvelope]:
        """Execute business logic for Handle Command codon"""
        if command.command_type == "create_greeting":
            return self._create_greeting_logic(command)
        else:
            raise ValueError(f"Unknown command type: {command.command_type}")

    def _execute_query_logic(self, query_command: SacredCommand) -> Dict[str, Any]:
        """Execute query logic for Query Data codon"""
        if query_command.command_type == "get_greeting_stats":
            return {
                "aggregate_id": self.id,
                "greeting_count": self.greeting_count,
                "total_greetings_sent": len(self.greetings_sent),
                "status": self.status,
                "last_greeting": self.last_greeting,
                "sacred_compliance": self._calculate_compliance_score(),
                "codon_statistics": self.get_codon_statistics(),
            }
        else:
            return super()._execute_query_logic(query_command)

    def _execute_reaction_logic(
        self, event: PollenEnvelope, reaction_command: SacredCommand
    ) -> List[PollenEnvelope]:
        """Execute reaction logic for React to Event codon"""
        if event.event_type in ["HelloHiveCreatedEvent", "GreetingReceivedEvent"]:
            return self._create_greeting_response_logic(event, reaction_command)
        else:
            return []

    def _execute_immune_logic(
        self, mutation_event: PollenEnvelope, immune_command: SacredCommand
    ) -> List[Dict[str, Any]]:
        """Execute immune response logic"""
        corrective_actions = []

        if mutation_event.event_type == "GreetingErrorEvent":
            # Handle greeting errors
            corrective_actions.append(
                {
                    "action": "reset_greeting_state",
                    "reason": "greeting_error_detected",
                    "previous_count": self.greeting_count,
                }
            )

            # Reset internal state
            self.greeting_count = max(0, self.greeting_count - 1)
            self.status = "error_recovered"

        return corrective_actions

    def _execute_choreography_logic(
        self, workflow_definition: Dict[str, Any]
    ) -> List[PollenEnvelope]:
        """Execute complex choreography workflow"""
        # For HelloHive, choreography might involve multi-step greeting sequences
        events = []

        if workflow_definition.get("type") == "greeting_sequence":
            steps = workflow_definition.get("steps", [])

            for step in steps:
                if step["action"] == "create_greeting":
                    # Create greeting event
                    greeting_event = self._create_event(
                        "ChoreographyGreetingCreated",
                        {
                            "step": step,
                            "sequence_id": workflow_definition.get("sequence_id"),
                        },
                    )
                    events.append(greeting_event)

        return events

    # Helper methods for business logic

    def _create_greeting_logic(self, command: SacredCommand) -> List[PollenEnvelope]:
        """Business logic for creating greetings"""
        greeting_data = command.payload

        # Validate greeting data
        if not greeting_data.get("message"):
            raise ValueError("Greeting message is required")

        # Update aggregate state
        self.greeting_count += 1
        self.last_greeting = greeting_data.get("message")
        self.greetings_sent.append(greeting_data)
        self.status = "active"

        # Create greeting event
        greeting_event = self._create_event(
            "HelloHiveCreatedEvent",
            {
                "message": greeting_data.get("message"),
                "sender": greeting_data.get("sender", "unknown"),
                "greeting_number": self.greeting_count,
                "command_id": command.command_id,
            },
        )

        return [greeting_event]

    def _create_greeting_response_logic(
        self, original_event: PollenEnvelope, reaction_command: SacredCommand
    ) -> List[PollenEnvelope]:
        """Business logic for responding to greetings"""
        original_payload = dict(original_event.payload)

        # Create response greeting
        response_message = f"Hello back to you! (responding to: {original_payload.get('message', 'unknown')})"

        # Update state
        self.greeting_count += 1
        self.last_greeting = response_message

        # Create response event
        response_event = self._create_event(
            "GreetingResponseCreated",
            {
                "original_event_id": original_event.event_id,
                "response_message": response_message,
                "response_number": self.greeting_count,
            },
        )

        return [response_event]

    def _create_event(
        self, event_type: str, payload_data: Dict[str, Any]
    ) -> PollenEnvelope:
        """Helper to create PollenEnvelope events with proper structure"""
        payload_struct = Struct()
        payload_struct.update(payload_data)

        timestamp = Timestamp()
        timestamp.FromDatetime(datetime.now(timezone.utc))

        return PollenEnvelope(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            event_version="1.0",
            aggregate_id=self.id,
            timestamp=timestamp,
            payload=payload_struct,
        )

    def _apply_event(self, event: PollenEnvelope) -> None:
        """
        Apply events to aggregate state.

        This method is called by the base Aggregate class and handles
        all the events that this aggregate can produce.
        """
        event_payload = dict(event.payload)

        if event.event_type == "HelloHiveCreatedEvent":
            # Event already applied during command processing
            print(f"✅ Applied {event.event_type} to aggregate {self.id}")

        elif event.event_type == "GreetingResponseCreated":
            # Event already applied during reaction processing
            print(f"✅ Applied {event.event_type} to aggregate {self.id}")

        elif event.event_type == "ChoreographyGreetingCreated":
            # Handle choreography events
            print(f"✅ Applied choreography event {event.event_type}")

        elif event.event_type == "CorrectiveActionExecuted":
            # Handle immune system corrective actions
            print(f"🏥 Applied corrective action: {event_payload}")

        else:
            print(f"⚠️ Warning: Unhandled event type {event.event_type}")


# Example usage demonstrating Sacred Codon patterns
def demonstrate_sacred_codons():
    """Demonstrate all Sacred Codon patterns with HelloHive"""

    # Create sacred aggregate
    hive_aggregate = HelloHiveSacredAggregate("hello-hive-sacred-001")

    print("🧬 Demonstrating Sacred Codon Patterns in HelloHive")
    print("=" * 60)

    # 1. Handle Command Codon (C→A→G)
    print("\n1. 🎯 Handle Command Codon (C→A→G)")
    greeting_events = hive_aggregate.create_greeting(
        {"message": "Hello, Sacred Hive!", "sender": "Claude", "priority": "high"}
    )
    print(f"   Created {len(greeting_events)} events")

    # 2. Query Data Codon (C→T→C)
    print("\n2. 🔍 Query Data Codon (C→T→C)")
    stats = hive_aggregate.get_greeting_stats()
    print(f"   Retrieved stats: {stats['greeting_count']} greetings sent")
    print(f"   Sacred compliance: {stats['sacred_compliance']:.2f}")

    # 3. React to Event Codon (G→C→A→G)
    print("\n3. 🎭 React to Event Codon (G→C→A→G)")
    # Simulate external greeting event
    external_event = hive_aggregate._create_event(
        "GreetingReceivedEvent",
        {"message": "Greetings from another hive!", "sender": "ExternalHive"},
    )
    response_events = hive_aggregate.respond_to_greeting(external_event)
    print(f"   Generated {len(response_events)} response events")

    # 4. Immune Response Codon (G→C→A→C)
    print("\n4. 🏥 Immune Response Codon (G→C→A→C)")
    # Simulate error event
    error_event = hive_aggregate._create_event(
        "GreetingErrorEvent",
        {"error": "invalid_greeting_format", "details": "Missing required fields"},
    )
    correction_events = hive_aggregate.handle_greeting_error(error_event)
    print(f"   Applied {len(correction_events)} corrective actions")

    # 5. Choreography Codon
    print("\n5. 🎪 Choreography Codon (Complex Workflow)")
    choreography_events = hive_aggregate.execute_choreography_codon(
        {
            "type": "greeting_sequence",
            "sequence_id": "seq-001",
            "steps": [
                {"action": "create_greeting", "message": "Step 1"},
                {"action": "create_greeting", "message": "Step 2"},
            ],
        }
    )
    print(f"   Executed choreography with {len(choreography_events)} events")

    # Final statistics
    print("\n📊 Final Sacred Codon Statistics:")
    final_stats = hive_aggregate.get_codon_statistics()
    print(f"   Total commands executed: {final_stats['total_commands']}")
    print(f"   Sacred compliance score: {final_stats['sacred_compliance']:.2f}")
    print(f"   Most used codon: {final_stats['most_used_codon']}")

    return hive_aggregate


if __name__ == "__main__":
    demonstrate_sacred_codons()
