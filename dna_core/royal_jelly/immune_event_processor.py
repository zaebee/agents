"""
Hive Adaptation Engine - Bio/Sci Nature Processor

This module connects the Hive's biological adaptation system with
real-time event processing, enabling organic detection and evolution
of architectural variations during event flow.

Integration with Sacred Codon patterns:
- Monitors all events flowing through the system like cellular sensors
- Detects architectural adaptations and beneficial mutations
- Triggers organic responses via Sacred Codon patterns
- Maintains genetic diversity while preserving core integrity
- Enables evolutionary pressure and natural selection of patterns
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import uuid
from datetime import datetime, timezone
import re

from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp
from dna_core.pollen_protocol_pb2 import PollenEnvelope
from .sacred_codon import (
    SacredAggregate,
    SacredCommand,
    SacredCodonType,
    create_sacred_command,
)


class AdaptationType(Enum):
    """Types of architectural adaptations detected by the hive's biological sensors"""

    CODON_EVOLUTION = "codon_evolution"  # Sacred Codon pattern adaptation
    STRUCTURE_VARIATION = "structure_variation"  # PollenEnvelope structural changes
    ORGANISM_ADAPTATION = "organism_adaptation"  # Aggregate behavioral changes
    WORKFLOW_INNOVATION = "workflow_innovation"  # Choreography pattern evolution
    TEMPORAL_DRIFT = "temporal_drift"  # Natural time-related variations
    MESSAGE_EVOLUTION = "message_evolution"  # Payload content adaptation
    PROTOCOL_EVOLUTION = "protocol_evolution"  # Natural protocol versioning


@dataclass
class AdaptationEvent:
    """Represents a detected architectural adaptation or evolutionary variation"""

    adaptation_id: str
    adaptation_type: AdaptationType
    fitness: float  # 0.0 to 1.0 - fitness score for natural selection
    description: str
    source_event: Optional[PollenEnvelope]
    source_organism: Optional[str]  # Source aggregate/organism
    observed_at: datetime
    evidence: Dict[str, Any]
    evolutionary_pressure: Optional[str] = None  # Selection pressure description
    beneficial: bool = False  # Whether this is a beneficial mutation


class HiveAdaptationEngine:
    """
    Bio-inspired adaptation engine for the Hive ecosystem.

    This engine observes all events flowing through the Hive system,
    detecting architectural adaptations and evolutionary variations,
    then triggering organic responses through Sacred Codon patterns.

    Operates like biological adaptation systems:
    - Recognizes beneficial vs. harmful adaptations
    - Applies evolutionary pressure for natural selection
    - Enables symbiotic relationships between organisms
    - Supports genetic diversity while maintaining core integrity
    """

    def __init__(self):
        self._adaptation_sensors: List[
            Callable[[PollenEnvelope], List[AdaptationEvent]]
        ] = []
        self._evolutionary_responders: Dict[
            AdaptationType, Callable[[AdaptationEvent], List[SacredCommand]]
        ] = {}
        self._adaptation_history: List[AdaptationEvent] = []
        self._enabled = True
        self._fitness_threshold = (
            0.3  # Adaptations below this fitness are naturally selected out
        )
        self._symbiosis_enabled = True  # Enable symbiotic relationships

        # Register default biological sensors and evolutionary responders
        self._register_default_sensors()
        self._register_default_evolutionary_responders()

    def process_event(
        self, event: PollenEnvelope, target_organism: Optional[SacredAggregate] = None
    ) -> List[SacredCommand]:
        """
        Process an event through the hive's adaptation sensors, detecting
        evolutionary variations and generating organic response commands.

        Returns a list of Sacred Commands for evolutionary responses.
        """
        if not self._enabled:
            return []

        evolutionary_commands = []

        # Run all adaptation sensors on the event
        detected_adaptations = []
        for sensor in self._adaptation_sensors:
            try:
                adaptations = sensor(event)
                detected_adaptations.extend(adaptations)
            except Exception as e:
                # Sensor itself might need recalibration - create a meta-adaptation
                meta_adaptation = AdaptationEvent(
                    adaptation_id=str(uuid.uuid4()),
                    adaptation_type=AdaptationType.ORGANISM_ADAPTATION,
                    fitness=0.2,
                    description=f"Adaptation sensor needs recalibration: {e}",
                    source_event=event,
                    source_organism=None,
                    observed_at=datetime.now(timezone.utc),
                    evidence={"sensor_error": str(e)},
                    evolutionary_pressure="sensor_maintenance_pressure",
                )
                detected_adaptations.append(meta_adaptation)

        # Apply natural selection - filter by fitness threshold
        fit_adaptations = [
            a for a in detected_adaptations if a.fitness >= self._fitness_threshold
        ]

        # Record adaptations in evolutionary history
        self._adaptation_history.extend(fit_adaptations)

        # Generate evolutionary responses for significant adaptations
        for adaptation in fit_adaptations:
            if adaptation.adaptation_type in self._evolutionary_responders:
                try:
                    response_commands = self._evolutionary_responders[
                        adaptation.adaptation_type
                    ](adaptation)
                    evolutionary_commands.extend(response_commands)
                except Exception as e:
                    # Evolutionary responder needs adaptation - create symbiotic command
                    symbiotic_command = self._create_symbiotic_adaptation_command(
                        adaptation, str(e)
                    )
                    evolutionary_commands.append(symbiotic_command)

        # If we have a target organism, execute evolutionary commands symbiotically
        if target_organism and evolutionary_commands:
            for command in evolutionary_commands:
                try:
                    # Convert evolutionary command to adaptation event for processing
                    adaptation_event = self._create_adaptation_event_from_command(
                        command, event
                    )
                    target_organism.execute_immune_response_codon(adaptation_event)
                except Exception as e:
                    print(f"🌱 Note: Evolutionary response adaptation needed: {e}")

        return evolutionary_commands

    def _register_default_sensors(self):
        """Register the default set of biological adaptation sensors"""

        # Codon Evolution Sensor
        def sense_codon_adaptations(event: PollenEnvelope) -> List[AdaptationEvent]:
            adaptations = []

            # Check for structural variations in event structure
            if not event.event_id:
                adaptations.append(
                    AdaptationEvent(
                        adaptation_id=str(uuid.uuid4()),
                        adaptation_type=AdaptationType.STRUCTURE_VARIATION,
                        fitness=0.1,  # Low fitness - may need structural evolution
                        description="Event structure variation: missing event_id",
                        source_event=event,
                        source_organism=event.aggregate_id
                        if event.aggregate_id
                        else None,
                        observed_at=datetime.now(timezone.utc),
                        evidence={"missing_field": "event_id"},
                        evolutionary_pressure="structural_integrity_pressure",
                    )
                )

            # Check for message evolution patterns (some may be beneficial)
            unusual_patterns = [
                r".*[Nn]ew.*",
                r".*[Ee]volved.*",
                r".*[Aa]daptive.*",
                r".*[Ii]nnovative.*",
                r".*[Ee]mergent.*",
                r".*[Mm]utated.*",
            ]

            for pattern in unusual_patterns:
                if re.search(pattern, event.event_type):
                    # Some patterns might be beneficial evolutionary adaptations
                    fitness_score = (
                        0.6
                        if "innovative" in pattern.lower()
                        or "evolved" in pattern.lower()
                        else 0.4
                    )
                    adaptations.append(
                        AdaptationEvent(
                            adaptation_id=str(uuid.uuid4()),
                            adaptation_type=AdaptationType.MESSAGE_EVOLUTION,
                            fitness=fitness_score,
                            description=f"Message evolution pattern observed: {pattern}",
                            source_event=event,
                            source_organism=event.aggregate_id,
                            observed_at=datetime.now(timezone.utc),
                            evidence={
                                "evolution_pattern": pattern,
                                "event_type": event.event_type,
                            },
                            beneficial=fitness_score > 0.5,
                        )
                    )

            return adaptations

        # Temporal Drift Sensor
        def sense_temporal_variations(event: PollenEnvelope) -> List[AdaptationEvent]:
            adaptations = []

            if event.timestamp:
                event_time = event.timestamp.ToDatetime()
                now = datetime.now(timezone.utc)

                # Check for temporal drift patterns (natural variation in distributed systems)
                future_threshold = 300  # 5 minutes
                if (event_time - now).total_seconds() > future_threshold:
                    # Temporal drift might indicate clock synchronization needs or distributed processing
                    fitness = 0.3  # Lower fitness but not necessarily harmful
                    adaptations.append(
                        AdaptationEvent(
                            adaptation_id=str(uuid.uuid4()),
                            adaptation_type=AdaptationType.TEMPORAL_DRIFT,
                            fitness=fitness,
                            description="Temporal drift observed: event from future timeframe",
                            source_event=event,
                            source_organism=event.aggregate_id,
                            observed_at=now,
                            evidence={
                                "event_time": event_time.isoformat(),
                                "current_time": now.isoformat(),
                                "drift_seconds": (event_time - now).total_seconds(),
                            },
                            evolutionary_pressure="temporal_synchronization_pressure",
                        )
                    )

                # Check for historical events (may represent delayed processing or archival data)
                old_threshold = 86400  # 24 hours
                if (now - event_time).total_seconds() > old_threshold:
                    # Old events might be part of historical data processing or recovery
                    fitness = 0.4  # Moderate fitness - may be legitimate
                    adaptations.append(
                        AdaptationEvent(
                            adaptation_id=str(uuid.uuid4()),
                            adaptation_type=AdaptationType.TEMPORAL_DRIFT,
                            fitness=fitness,
                            description="Historical event processing observed",
                            source_event=event,
                            source_organism=event.aggregate_id,
                            observed_at=now,
                            evidence={
                                "event_time": event_time.isoformat(),
                                "age_seconds": (now - event_time).total_seconds(),
                            },
                            evolutionary_pressure="data_archival_pressure",
                        )
                    )

            return adaptations

        # Protocol Evolution Sensor
        def sense_protocol_evolution(event: PollenEnvelope) -> List[AdaptationEvent]:
            adaptations = []

            # Check for protocol version evolution
            expected_versions = ["1.0", "1.1", "2.0"]
            if event.event_version not in expected_versions:
                # New versions might represent beneficial protocol evolution
                fitness = 0.7 if event.event_version > "2.0" else 0.4
                adaptations.append(
                    AdaptationEvent(
                        adaptation_id=str(uuid.uuid4()),
                        adaptation_type=AdaptationType.PROTOCOL_EVOLUTION,
                        fitness=fitness,
                        description=f"Protocol evolution observed: version {event.event_version}",
                        source_event=event,
                        source_organism=event.aggregate_id,
                        observed_at=datetime.now(timezone.utc),
                        evidence={
                            "evolved_version": event.event_version,
                            "known_versions": expected_versions,
                        },
                        evolutionary_pressure="protocol_compatibility_pressure",
                        beneficial=fitness > 0.5,
                    )
                )

            return adaptations

        # Register all biological sensors
        self._adaptation_sensors = [
            sense_codon_adaptations,
            sense_temporal_variations,
            sense_protocol_evolution,
        ]

    def _register_default_evolutionary_responders(self):
        """Register default evolutionary response generators - organic adaptation strategies"""

        def respond_to_structure_variation(
            adaptation: AdaptationEvent,
        ) -> List[SacredCommand]:
            """Generate evolutionary response for structural variations"""
            return [
                create_sacred_command(
                    command_type="evolve_structure_adaptation",
                    payload={
                        "adaptation_id": adaptation.adaptation_id,
                        "fitness": adaptation.fitness,
                        "evidence": adaptation.evidence,
                        "action": "evolve_structure",
                        "evolutionary_pressure": adaptation.evolutionary_pressure,
                        "beneficial": adaptation.beneficial,
                    },
                    codon_type=SacredCodonType.IMMUNE_RESPONSE,
                    source="hive_adaptation_structure_responder",
                )
            ]

        def respond_to_message_evolution(
            adaptation: AdaptationEvent,
        ) -> List[SacredCommand]:
            """Generate evolutionary response for message adaptations"""
            return [
                create_sacred_command(
                    command_type="nurture_message_evolution",
                    payload={
                        "adaptation_id": adaptation.adaptation_id,
                        "fitness": adaptation.fitness,
                        "evolution_pattern": adaptation.evidence.get(
                            "evolution_pattern"
                        ),
                        "action": "cultivate" if adaptation.beneficial else "observe",
                        "symbiotic_potential": adaptation.fitness > 0.6,
                    },
                    codon_type=SacredCodonType.IMMUNE_RESPONSE,
                    source="hive_adaptation_message_responder",
                )
            ]

        def respond_to_temporal_drift(
            adaptation: AdaptationEvent,
        ) -> List[SacredCommand]:
            """Generate evolutionary response for temporal variations"""
            return [
                create_sacred_command(
                    command_type="harmonize_temporal_rhythm",
                    payload={
                        "adaptation_id": adaptation.adaptation_id,
                        "fitness": adaptation.fitness,
                        "temporal_evidence": adaptation.evidence,
                        "action": "synchronize_naturally",
                        "rhythm_adjustment": True,
                        "distributed_harmony": True,
                    },
                    codon_type=SacredCodonType.IMMUNE_RESPONSE,
                    source="hive_adaptation_temporal_responder",
                )
            ]

        def respond_to_protocol_evolution(
            adaptation: AdaptationEvent,
        ) -> List[SacredCommand]:
            """Generate evolutionary response for protocol evolution"""
            return [
                create_sacred_command(
                    command_type="embrace_protocol_evolution",
                    payload={
                        "adaptation_id": adaptation.adaptation_id,
                        "fitness": adaptation.fitness,
                        "version_evidence": adaptation.evidence,
                        "evolutionary_pressure": adaptation.evolutionary_pressure,
                        "action": "co_evolve"
                        if adaptation.beneficial
                        else "assess_compatibility",
                    },
                    codon_type=SacredCodonType.IMMUNE_RESPONSE,
                    source="hive_adaptation_protocol_responder",
                )
            ]

        # Map adaptation types to their evolutionary responders
        self._evolutionary_responders = {
            AdaptationType.STRUCTURE_VARIATION: respond_to_structure_variation,
            AdaptationType.MESSAGE_EVOLUTION: respond_to_message_evolution,
            AdaptationType.TEMPORAL_DRIFT: respond_to_temporal_drift,
            AdaptationType.PROTOCOL_EVOLUTION: respond_to_protocol_evolution,
        }

    def _create_symbiotic_adaptation_command(
        self, adaptation: AdaptationEvent, error: str
    ) -> SacredCommand:
        """Create symbiotic adaptation when normal evolutionary responders need recalibration"""
        return create_sacred_command(
            command_type="symbiotic_adaptation_response",
            payload={
                "adaptation_id": adaptation.adaptation_id,
                "recalibration_needed": error,
                "fitness": 0.8,  # High fitness for adaptive systems
                "action": "symbiotic_learning",
                "collaboration_opportunity": True,
                "organic_adaptation_required": True,
            },
            codon_type=SacredCodonType.IMMUNE_RESPONSE,
            source="hive_adaptation_symbiosis",
        )

    def _create_adaptation_event_from_command(
        self, command: SacredCommand, original_event: PollenEnvelope
    ) -> PollenEnvelope:
        """Convert an evolutionary command back to a PollenEnvelope for processing"""
        payload_struct = Struct()
        payload_struct.update(
            {
                "evolutionary_command": command.command_type,
                "adaptation_details": command.payload,
                "original_event_id": original_event.event_id,
                "evolutionary_response_id": command.command_id,
            }
        )

        timestamp = Timestamp()
        timestamp.FromDatetime(command.timestamp)

        return PollenEnvelope(
            event_id=str(uuid.uuid4()),
            event_type="HiveAdaptationObserved",
            event_version="1.0",
            aggregate_id=original_event.aggregate_id,
            timestamp=timestamp,
            payload=payload_struct,
        )

    def register_custom_sensor(
        self, sensor: Callable[[PollenEnvelope], List[AdaptationEvent]]
    ):
        """Register a custom adaptation sensor"""
        self._adaptation_sensors.append(sensor)

    def register_custom_responder(
        self,
        adaptation_type: AdaptationType,
        responder: Callable[[AdaptationEvent], List[SacredCommand]],
    ):
        """Register a custom evolutionary responder for a specific adaptation type"""
        self._evolutionary_responders[adaptation_type] = responder

    def get_adaptation_history(
        self,
        adaptation_type: Optional[AdaptationType] = None,
        since: Optional[datetime] = None,
    ) -> List[AdaptationEvent]:
        """Get history of observed adaptations with optional filtering"""
        history = self._adaptation_history

        if adaptation_type:
            history = [a for a in history if a.adaptation_type == adaptation_type]

        if since:
            history = [a for a in history if a.observed_at >= since]

        return history

    def get_adaptation_statistics(self) -> Dict[str, Any]:
        """Get statistics about hive adaptation activity"""
        if not self._adaptation_history:
            return {
                "total_adaptations": 0,
                "adaptation_types": {},
                "average_fitness": 0.0,
                "most_common_adaptation": None,
                "adaptation_efficiency": 1.0,
                "beneficial_adaptations": 0,
            }

        adaptation_counts = {}
        total_fitness = 0.0
        beneficial_count = 0

        for adaptation in self._adaptation_history:
            adapt_type = adaptation.adaptation_type.value
            adaptation_counts[adapt_type] = adaptation_counts.get(adapt_type, 0) + 1
            total_fitness += adaptation.fitness
            if adaptation.beneficial:
                beneficial_count += 1

        most_common = max(adaptation_counts.items(), key=lambda x: x[1])[0]
        avg_fitness = total_fitness / len(self._adaptation_history)

        # Adaptation efficiency: ratio of beneficial to low-fitness adaptations
        # Higher efficiency means promoting healthy evolution
        high_fitness = len([a for a in self._adaptation_history if a.fitness >= 0.6])
        low_fitness = len([a for a in self._adaptation_history if a.fitness < 0.3])
        efficiency = high_fitness / max(1, low_fitness)

        return {
            "total_adaptations": len(self._adaptation_history),
            "adaptation_types": adaptation_counts,
            "average_fitness": avg_fitness,
            "most_common_adaptation": most_common,
            "adaptation_efficiency": min(1.0, efficiency),
            "beneficial_adaptations": beneficial_count,
            "sensors_active": len(self._adaptation_sensors),
            "responders_registered": len(self._evolutionary_responders),
            "symbiosis_enabled": self._symbiosis_enabled,
        }

    def set_fitness_threshold(self, threshold: float):
        """Set the fitness threshold for adaptation selection (0.0 to 1.0)"""
        self._fitness_threshold = max(0.0, min(1.0, threshold))

    def enable_adaptation_engine(self):
        """Enable the adaptation engine processing"""
        self._enabled = True

    def disable_adaptation_engine(self):
        """Disable the adaptation engine processing (for system maintenance)"""
        self._enabled = False

    def enable_symbiosis(self):
        """Enable symbiotic relationships between adaptations"""
        self._symbiosis_enabled = True

    def disable_symbiosis(self):
        """Disable symbiotic relationships (for isolation testing)"""
        self._symbiosis_enabled = False


# Global hive adaptation engine instance
_global_adaptation_engine = None


def get_adaptation_engine() -> HiveAdaptationEngine:
    """Get the global hive adaptation engine instance"""
    global _global_adaptation_engine
    if _global_adaptation_engine is None:
        _global_adaptation_engine = HiveAdaptationEngine()
    return _global_adaptation_engine


def process_event_with_adaptation_engine(
    event: PollenEnvelope, target_organism: Optional[SacredAggregate] = None
) -> List[SacredCommand]:
    """Convenience function to process an event through the hive's adaptation engine"""
    return get_adaptation_engine().process_event(event, target_organism)


# Legacy compatibility functions (deprecated - use adaptation engine instead)
def get_immune_processor() -> HiveAdaptationEngine:
    """Legacy function - use get_adaptation_engine() instead"""
    return get_adaptation_engine()


def process_event_with_immune_system(
    event: PollenEnvelope, target_aggregate: Optional[SacredAggregate] = None
) -> List[SacredCommand]:
    """Legacy function - use process_event_with_adaptation_engine() instead"""
    return process_event_with_adaptation_engine(event, target_aggregate)


# Legacy compatibility aliases
ImmuneEventProcessor = HiveAdaptationEngine
MutationEvent = AdaptationEvent
MutationType = AdaptationType
