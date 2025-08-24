"""
Sacred Codon Implementation for Hive Architecture

This module implements the 5 Sacred Codons as defined in PATTERNS.md:
1. Handle Command (C→A→G) - To change the world
2. Query Data (C→T→C) - To see the world
3. React to Event (G→C→A→G) - To listen to the world
4. Immune Response (G→C→A→C) - To heal the world
5. Choreography - Complex multi-step workflows (To become)

These patterns ensure all components follow the sacred genetic architecture.
"""

from typing import List, Dict, Any, Optional, Callable
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
import uuid
from datetime import datetime, timezone

from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp
from dna_core.pollen_protocol_pb2 import PollenEnvelope
from .aggregate import Aggregate


class SacredCodonType(Enum):
    """The Sacred Codons from PATTERNS.md plus bio/sci extensions"""

    HANDLE_COMMAND = "handle_command"  # C→A→G (to change)
    QUERY_DATA = "query_data"  # C→T→C (to see)
    REACT_TO_EVENT = "react_to_event"  # G→C→A→G (to listen)
    IMMUNE_RESPONSE = "immune_response"  # G→C→A→C (to heal)
    CHOREOGRAPHY = "choreography"  # Complex workflows (to become)
    NEURAL_RESPONSE = "neural_response"  # Neural network processing responses
    CHEMICAL_REACTION = "chemical_reaction"  # Chemical bond formation/breaking
    QUANTUM_SUPERPOSITION = "quantum_superposition"  # Quantum superposition state operations


@dataclass
class SacredCommand:
    """Base class for commands that follow Sacred Codon patterns"""

    command_id: str
    command_type: str
    payload: Dict[str, Any]
    codon_type: SacredCodonType
    timestamp: datetime
    source: str = "unknown"


@dataclass
class CodonValidationResult:
    """Result of Sacred Codon pattern validation"""

    is_valid: bool
    codon_type: SacredCodonType
    pattern_sequence: str
    violations: List[str]
    confidence: float = 1.0


class SacredAggregate(Aggregate):
    """
    Enhanced Aggregate that implements Sacred Codon patterns.

    This class extends Jules' base Aggregate with explicit Sacred Codon
    pattern validation and execution, ensuring all domain operations
    follow the sacred genetic architecture of the Hive.
    """

    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
        self._codon_history: List[SacredCommand] = []
        self._validation_enabled = True
        self._immune_monitoring_enabled = True

    def execute_handle_command_codon(
        self, command: SacredCommand
    ) -> List[PollenEnvelope]:
        """
        Sacred Codon: Handle Command (C→A→G)

        The fundamental pattern for changing state:
        1. C (Connector) receives external command
        2. A (Aggregate) processes and validates
        3. G (Genesis Event) records the change

        This is the only way state should change in the system.
        """
        if command.codon_type != SacredCodonType.HANDLE_COMMAND:
            raise ValueError(f"Expected HANDLE_COMMAND codon, got {command.codon_type}")

        # Validate the C→A→G pattern
        validation = self._validate_codon_pattern(command, "C→A→G")
        if not validation.is_valid:
            raise ValueError(f"Sacred Codon violation: {validation.violations}")

        # Record the command in our codon history
        self._codon_history.append(command)

        # Execute business logic (A step)
        events = self._execute_command_logic(command)

        # Record all events (G step)
        for event in events:
            self._record_event(event)

        return events

    def execute_query_data_codon(self, query_command: SacredCommand) -> Dict[str, Any]:
        """
        Sacred Codon: Query Data (C→T→C)

        The pattern for reading state without side effects:
        1. C (Connector) receives query request
        2. T (Transformation) processes the query
        3. C (Connector) returns the result

        This pattern must be pure - no state changes allowed.
        """
        if query_command.codon_type != SacredCodonType.QUERY_DATA:
            raise ValueError(
                f"Expected QUERY_DATA codon, got {query_command.codon_type}"
            )

        # Validate the C→T→C pattern
        validation = self._validate_codon_pattern(query_command, "C→T→C")
        if not validation.is_valid:
            raise ValueError(f"Sacred Codon violation: {validation.violations}")

        # Execute pure transformation (T step) - no state mutation
        result = self._execute_query_logic(query_command)

        # Return through connector (C step)
        return result

    def execute_react_to_event_codon(
        self, genesis_event: PollenEnvelope
    ) -> List[PollenEnvelope]:
        """
        Sacred Codon: React to Event (G→C→A→G)

        The pattern for event-driven choreography:
        1. G (Genesis Event) arrives from another component
        2. C (Connector) translates event to internal command
        3. A (Aggregate) processes the reaction
        4. G (Genesis Event) records the reaction

        This enables loose coupling between components.
        """
        # Convert event to internal command (C step)
        reaction_command = self._translate_event_to_command(genesis_event)

        if reaction_command.codon_type != SacredCodonType.REACT_TO_EVENT:
            reaction_command.codon_type = SacredCodonType.REACT_TO_EVENT

        # Validate the G→C→A→G pattern
        validation = self._validate_codon_pattern(reaction_command, "G→C→A→G")
        if not validation.is_valid:
            raise ValueError(f"Sacred Codon violation: {validation.violations}")

        # Record the reaction command
        self._codon_history.append(reaction_command)

        # Execute reaction logic (A step)
        reaction_events = self._execute_reaction_logic(genesis_event, reaction_command)

        # Record all reaction events (G step)
        for event in reaction_events:
            self._record_event(event)

        return reaction_events

    def execute_immune_response_codon(
        self, mutation_event: PollenEnvelope
    ) -> List[PollenEnvelope]:
        """
        Sacred Codon: Immune Response (G→C→A→C)

        The pattern for self-healing and mutation correction:
        1. G (Genesis Event) signals a mutation or failure
        2. C (Connector) translates to immune response command
        3. A (Aggregate) determines corrective action
        4. C (Connector) executes corrective command

        This pattern enables the Hive's immune system.
        """
        # Convert mutation event to immune command (C step)
        immune_command = self._translate_mutation_to_command(mutation_event)
        immune_command.codon_type = SacredCodonType.IMMUNE_RESPONSE

        # Validate the G→C→A→C pattern
        validation = self._validate_codon_pattern(immune_command, "G→C→A→C")
        if not validation.is_valid:
            raise ValueError(f"Sacred Codon violation: {validation.violations}")

        # Record the immune command
        self._codon_history.append(immune_command)

        # Execute immune logic (A step)
        corrective_actions = self._execute_immune_logic(mutation_event, immune_command)

        # Execute corrective actions through connector (C step)
        correction_events = self._execute_corrective_actions(corrective_actions)

        return correction_events

    def execute_choreography_codon(
        self, workflow_definition: Dict[str, Any]
    ) -> List[PollenEnvelope]:
        """
        Sacred Codon: Choreography (Complex Multi-Step)

        The pattern for complex workflows and orchestration:
        This implements sophisticated multi-step processes that may involve
        multiple other Sacred Codons in sequence.

        This is the "becoming" pattern - for complex transformations.
        """
        choreography_command = SacredCommand(
            command_id=str(uuid.uuid4()),
            command_type="choreography",
            payload=workflow_definition,
            codon_type=SacredCodonType.CHOREOGRAPHY,
            timestamp=datetime.now(timezone.utc),
            source="choreography_engine",
        )

        # Validate choreography pattern
        validation = self._validate_codon_pattern(
            choreography_command, "COMPLEX_WORKFLOW"
        )
        if not validation.is_valid:
            raise ValueError(f"Sacred Codon violation: {validation.violations}")

        # Record the choreography command
        self._codon_history.append(choreography_command)

        # Execute complex workflow
        workflow_events = self._execute_choreography_logic(workflow_definition)

        # Record all workflow events
        for event in workflow_events:
            self._record_event(event)

        return workflow_events

    def _validate_codon_pattern(
        self, command: SacredCommand, expected_pattern: str
    ) -> CodonValidationResult:
        """Validate that a command follows the expected Sacred Codon pattern"""
        violations = []
        confidence = 1.0

        # Basic validation
        if not command.command_id:
            violations.append("Command missing unique ID")
            confidence -= 0.2

        if not command.payload:
            violations.append("Command missing payload data")
            confidence -= 0.1

        # Pattern-specific validation
        if expected_pattern == "C→A→G":
            # Handle Command pattern validation
            if not hasattr(self, "_execute_command_logic"):
                violations.append("Aggregate missing command execution logic")
                confidence -= 0.3

        elif expected_pattern == "C→T→C":
            # Query Data pattern validation
            if not hasattr(self, "_execute_query_logic"):
                violations.append("Aggregate missing query execution logic")
                confidence -= 0.3

        elif expected_pattern == "G→C→A→G":
            # React to Event pattern validation
            if not hasattr(self, "_execute_reaction_logic"):
                violations.append("Aggregate missing reaction logic")
                confidence -= 0.3

        elif expected_pattern == "G→C→A→C":
            # Immune Response pattern validation
            if not hasattr(self, "_execute_immune_logic"):
                violations.append("Aggregate missing immune response logic")
                confidence -= 0.3

        is_valid = len(violations) == 0 and confidence >= 0.7

        return CodonValidationResult(
            is_valid=is_valid,
            codon_type=command.codon_type,
            pattern_sequence=expected_pattern,
            violations=violations,
            confidence=max(0.0, confidence),
        )

    def get_codon_history(self) -> List[SacredCommand]:
        """Get the history of all Sacred Codon executions"""
        return self._codon_history.copy()

    def get_codon_statistics(self) -> Dict[str, Any]:
        """Get statistics about Sacred Codon usage"""
        codon_counts = {}
        for codon_type in SacredCodonType:
            codon_counts[codon_type.value] = len(
                [cmd for cmd in self._codon_history if cmd.codon_type == codon_type]
            )

        return {
            "total_commands": len(self._codon_history),
            "codon_counts": codon_counts,
            "most_used_codon": max(codon_counts.items(), key=lambda x: x[1])[0]
            if codon_counts
            else None,
            "sacred_compliance": self._calculate_compliance_score(),
        }

    def _calculate_compliance_score(self) -> float:
        """Calculate how well this aggregate follows Sacred Codon patterns"""
        if not self._codon_history:
            return 0.0

        # Basic compliance - all commands follow codon patterns
        valid_commands = len([cmd for cmd in self._codon_history if cmd.codon_type])
        compliance = valid_commands / len(self._codon_history)

        # Bonus for using multiple codon types (variety)
        unique_codons = len(set(cmd.codon_type for cmd in self._codon_history))
        variety_bonus = min(0.2, unique_codons * 0.05)

        return min(1.0, compliance + variety_bonus)

    # Abstract methods that specific aggregates must implement

    @abstractmethod
    def _execute_command_logic(self, command: SacredCommand) -> List[PollenEnvelope]:
        """Execute the business logic for a Handle Command codon"""
        pass

    def _execute_query_logic(self, query_command: SacredCommand) -> Dict[str, Any]:
        """Execute the query logic for a Query Data codon"""
        # Default implementation returns empty result
        return {"result": "not_implemented", "query_id": query_command.command_id}

    def _execute_reaction_logic(
        self, event: PollenEnvelope, reaction_command: SacredCommand
    ) -> List[PollenEnvelope]:
        """Execute the reaction logic for a React to Event codon"""
        # Default implementation returns empty list
        return []

    def _execute_immune_logic(
        self, mutation_event: PollenEnvelope, immune_command: SacredCommand
    ) -> List[Dict[str, Any]]:
        """Execute the immune response logic"""
        # Default implementation returns empty list
        return []

    def _execute_choreography_logic(
        self, workflow_definition: Dict[str, Any]
    ) -> List[PollenEnvelope]:
        """Execute complex choreography workflow"""
        # Default implementation returns empty list
        return []

    def _translate_event_to_command(self, event: PollenEnvelope) -> SacredCommand:
        """Convert a Genesis Event into an internal command"""
        return SacredCommand(
            command_id=str(uuid.uuid4()),
            command_type=f"react_to_{event.event_type}",
            payload=dict(event.payload),
            codon_type=SacredCodonType.REACT_TO_EVENT,
            timestamp=datetime.now(timezone.utc),
            source=f"event_reaction_{event.event_id}",
        )

    def _translate_mutation_to_command(
        self, mutation_event: PollenEnvelope
    ) -> SacredCommand:
        """Convert a mutation event into an immune response command"""
        return SacredCommand(
            command_id=str(uuid.uuid4()),
            command_type=f"immune_response_to_{mutation_event.event_type}",
            payload=dict(mutation_event.payload),
            codon_type=SacredCodonType.IMMUNE_RESPONSE,
            timestamp=datetime.now(timezone.utc),
            source=f"immune_system_{mutation_event.event_id}",
        )

    def _execute_corrective_actions(
        self, corrective_actions: List[Dict[str, Any]]
    ) -> List[PollenEnvelope]:
        """Execute corrective actions and return resulting events"""
        events = []

        for action in corrective_actions:
            # Create a corrective action event
            payload_struct = Struct()
            payload_struct.update(action)

            timestamp = Timestamp()
            timestamp.FromDatetime(datetime.now(timezone.utc))

            event = PollenEnvelope(
                event_id=str(uuid.uuid4()),
                event_type="CorrectiveActionExecuted",
                event_version="1.0",
                aggregate_id=self.id,
                timestamp=timestamp,
                payload=payload_struct,
            )

            events.append(event)

        return events

    def _record_event(self, event: PollenEnvelope) -> None:
        """Override base _record_event to add immune system monitoring"""
        # Process through immune system first if monitoring is enabled
        if self._immune_monitoring_enabled:
            try:
                # Import here to avoid circular dependencies
                from .immune_event_processor import process_event_with_immune_system

                immune_commands = process_event_with_immune_system(event, self)

                # Log immune system activity
                if immune_commands:
                    print(
                        f"🦠 Immune system detected mutations in event {event.event_id}"
                    )
                    print(f"   Generated {len(immune_commands)} immune responses")

            except ImportError:
                # Immune system not available, continue without it
                pass
            except Exception as e:
                print(f"⚠️ Immune system error: {e}")

        # Continue with normal event recording
        super()._record_event(event)

    def enable_immune_monitoring(self):
        """Enable immune system monitoring for this aggregate"""
        self._immune_monitoring_enabled = True

    def disable_immune_monitoring(self):
        """Disable immune system monitoring for this aggregate"""
        self._immune_monitoring_enabled = False

    def get_immune_status(self) -> Dict[str, Any]:
        """Get immune system status for this aggregate"""
        try:
            from .immune_event_processor import get_immune_processor

            processor = get_immune_processor()

            # Get mutations related to this aggregate
            aggregate_mutations = [
                m
                for m in processor.get_mutation_history()
                if m.source_aggregate == self.id
            ]

            return {
                "monitoring_enabled": self._immune_monitoring_enabled,
                "mutations_detected": len(aggregate_mutations),
                "last_mutation": aggregate_mutations[-1].detected_at.isoformat()
                if aggregate_mutations
                else None,
                "immune_health": "healthy"
                if len(aggregate_mutations) == 0
                else "mutations_detected",
            }

        except ImportError:
            return {"monitoring_enabled": False, "error": "immune_system_not_available"}


def create_sacred_command(
    command_type: str,
    payload: Dict[str, Any],
    codon_type: SacredCodonType,
    source: str = "unknown",
) -> SacredCommand:
    """Helper function to create Sacred Commands with proper structure"""
    return SacredCommand(
        command_id=str(uuid.uuid4()),
        command_type=command_type,
        payload=payload,
        codon_type=codon_type,
        timestamp=datetime.now(timezone.utc),
        source=source,
    )
