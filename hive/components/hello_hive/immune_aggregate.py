"""
Enhanced HelloHive Aggregate with Integrated Immune System

This demonstrates how the Hive's Immune System integrates with Sacred Codon
patterns to provide real-time mutation detection and correction during
event processing.

Integration Features:
- Real-time event monitoring for architectural mutations
- Automatic immune responses via Sacred Codon patterns
- Collaborative validation with immune system feedback
- Temporal anomaly detection and correction
- Payload contamination scanning
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
    ImmuneEventProcessor,
    MutationType,
    get_immune_processor,
    process_event_with_immune_system,
)
from .command import HelloHiveCommand


class HelloHiveImmuneAggregate(SacredAggregate):
    """
    HelloHive Aggregate with integrated immune system monitoring.

    This aggregate demonstrates:
    - Sacred Codon patterns with immune system integration
    - Real-time mutation detection during event processing
    - Automatic immune responses to architectural violations
    - Comprehensive health monitoring and reporting

    The immune system operates transparently, monitoring all events
    for architectural mutations while maintaining the Sacred Codon
    patterns for proper genetic architecture compliance.
    """

    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
        self.greeting_count = 0
        self.greetings_sent = []
        self.status = "initialized"
        self.last_greeting = None
        self.immune_incidents = []

        # Configure immune system for this aggregate
        self._configure_immune_system()

    def create_greeting_with_immune_monitoring(
        self, greeting_data: Dict[str, Any]
    ) -> List[PollenEnvelope]:
        """
        Create a greeting with full immune system monitoring.

        This demonstrates Sacred Codon: Handle Command (C→A→G) with
        integrated immune system monitoring throughout the process.
        """
        print(f"\n🧬 Creating greeting with immune monitoring for aggregate {self.id}")

        # Create Sacred Command
        command = create_sacred_command(
            command_type="create_greeting_with_monitoring",
            payload=greeting_data,
            codon_type=SacredCodonType.HANDLE_COMMAND,
            source="hello_hive_immune_connector",
        )

        # Execute with immune monitoring
        events = self.execute_handle_command_codon(command)

        # Report immune status
        immune_status = self.get_immune_status()
        print(f"🏥 Immune status: {immune_status['immune_health']}")
        if immune_status["mutations_detected"] > 0:
            print(f"   Mutations detected: {immune_status['mutations_detected']}")

        return events

    def simulate_mutation_event(
        self, mutation_type: str = "temporal_anomaly"
    ) -> List[PollenEnvelope]:
        """
        Simulate a mutation event to demonstrate immune system response.

        This creates intentionally malformed events to trigger the immune system
        and demonstrate the G→C→A→C Sacred Codon pattern for immune response.
        """
        print(f"\n🦠 Simulating {mutation_type} mutation event")

        if mutation_type == "temporal_anomaly":
            # Create event with future timestamp (should trigger immune response)
            future_time = datetime.now(timezone.utc).replace(year=2050)
            timestamp = Timestamp()
            timestamp.FromDatetime(future_time)

            malformed_event = PollenEnvelope(
                event_id=str(uuid.uuid4()),
                event_type="MalformedGreetingEvent",
                event_version="1.0",
                aggregate_id=self.id,
                timestamp=timestamp,  # Future timestamp - should trigger immune response
                payload=Struct(),
            )

        elif mutation_type == "payload_contamination":
            # Create event with suspicious payload
            payload_struct = Struct()
            payload_struct.update(
                {
                    "message": "Hello from virus scanner",  # Should trigger contamination detector
                    "sender": "HackBot",
                    "malware_signature": "suspicious_pattern",
                }
            )

            malformed_event = PollenEnvelope(
                event_id=str(uuid.uuid4()),
                event_type="ContaminatedGreetingEvent",
                event_version="1.0",
                aggregate_id=self.id,
                timestamp=Timestamp(),
                payload=payload_struct,
            )

        elif mutation_type == "event_malformation":
            # Create event missing required fields
            malformed_event = PollenEnvelope(
                event_id="",  # Missing event_id - should trigger immune response
                event_type="MalformedEvent",
                event_version="1.0",
                aggregate_id=self.id,
                payload=Struct(),
            )

        else:
            # Protocol drift - unknown version
            malformed_event = PollenEnvelope(
                event_id=str(uuid.uuid4()),
                event_type="UnknownVersionEvent",
                event_version="99.9",  # Unknown version - should trigger immune response
                aggregate_id=self.id,
                timestamp=Timestamp(),
                payload=Struct(),
            )

        # Process through immune system (this should trigger responses)
        immune_commands = process_event_with_immune_system(malformed_event, self)

        print(f"🔬 Immune system analysis complete:")
        print(f"   Detected mutations: {len(immune_commands)}")

        # Convert the malformed event to immune response via Sacred Codon
        if immune_commands:
            print(f"🏥 Executing immune responses via Sacred Codon patterns")
            immune_events = self.execute_immune_response_codon(malformed_event)
            return immune_events
        else:
            print(f"✅ No immune response needed")
            return []

    def get_comprehensive_health_report(self) -> Dict[str, Any]:
        """
        Get comprehensive health report including Sacred Codon compliance
        and immune system status.
        """
        # Get basic Sacred Codon statistics
        codon_stats = self.get_codon_statistics()

        # Get immune system status
        immune_status = self.get_immune_status()

        # Get global immune processor statistics
        try:
            processor = get_immune_processor()
            global_stats = processor.get_immune_statistics()
        except:
            global_stats = {"error": "immune_processor_unavailable"}

        return {
            "aggregate_id": self.id,
            "greeting_stats": {
                "total_greetings": self.greeting_count,
                "greetings_sent": len(self.greetings_sent),
                "status": self.status,
                "last_greeting": self.last_greeting,
            },
            "sacred_codon_compliance": codon_stats,
            "immune_system_status": immune_status,
            "global_immune_stats": global_stats,
            "health_score": self._calculate_overall_health_score(
                codon_stats, immune_status
            ),
            "recommendations": self._generate_health_recommendations(
                codon_stats, immune_status
            ),
        }

    def _configure_immune_system(self):
        """Configure immune system with HelloHive-specific detectors"""
        try:
            processor = get_immune_processor()

            # Register custom detector for HelloHive-specific mutations
            def detect_greeting_mutations(event: PollenEnvelope) -> List:
                from dna_core.royal_jelly.immune_event_processor import MutationEvent

                mutations = []

                # Check for greeting-specific violations
                if event.event_type.startswith(
                    "HelloHive"
                ) or event.event_type.startswith("Greeting"):
                    payload_dict = dict(event.payload) if event.payload else {}

                    # Check for suspicious greeting content
                    message = payload_dict.get("message", "")
                    if any(
                        word in message.lower()
                        for word in ["hack", "virus", "malware", "attack"]
                    ):
                        mutations.append(
                            MutationEvent(
                                mutation_id=str(uuid.uuid4()),
                                mutation_type=MutationType.PAYLOAD_CONTAMINATION,
                                severity=0.9,
                                description="Suspicious content in greeting message",
                                source_event=event,
                                source_aggregate=event.aggregate_id,
                                detected_at=datetime.now(timezone.utc),
                                evidence={"suspicious_message": message},
                                suggested_correction="Sanitize greeting message content",
                            )
                        )

                return mutations

            processor.register_custom_detector(detect_greeting_mutations)
            print(f"🔧 Configured immune system for aggregate {self.id}")

        except Exception as e:
            print(f"⚠️ Failed to configure immune system: {e}")

    def _calculate_overall_health_score(
        self, codon_stats: Dict[str, Any], immune_status: Dict[str, Any]
    ) -> float:
        """Calculate overall health score (0.0 to 1.0)"""
        # Sacred Codon compliance score
        codon_score = codon_stats.get("sacred_compliance", 0.0)

        # Immune health score (inverse of mutations)
        mutations = immune_status.get("mutations_detected", 0)
        immune_score = max(
            0.0, 1.0 - (mutations * 0.1)
        )  # Each mutation reduces score by 0.1

        # Monitoring status bonus
        monitoring_bonus = (
            0.1 if immune_status.get("monitoring_enabled", False) else 0.0
        )

        # Weighted average
        overall_score = (codon_score * 0.6) + (immune_score * 0.3) + monitoring_bonus

        return min(1.0, overall_score)

    def _generate_health_recommendations(
        self, codon_stats: Dict[str, Any], immune_status: Dict[str, Any]
    ) -> List[str]:
        """Generate health recommendations based on current status"""
        recommendations = []

        # Sacred Codon recommendations
        codon_compliance = codon_stats.get("sacred_compliance", 0.0)
        if codon_compliance < 0.8:
            recommendations.append("Improve Sacred Codon pattern compliance")

        # Immune system recommendations
        mutations = immune_status.get("mutations_detected", 0)
        if mutations > 0:
            recommendations.append(
                f"Address {mutations} detected architectural mutations"
            )

        if not immune_status.get("monitoring_enabled", False):
            recommendations.append("Enable immune system monitoring")

        # Codon variety recommendations
        codon_counts = codon_stats.get("codon_counts", {})
        used_codons = len([count for count in codon_counts.values() if count > 0])
        if used_codons < 3:
            recommendations.append(
                "Utilize more Sacred Codon patterns for better architecture"
            )

        if not recommendations:
            recommendations.append(
                "System health is optimal - continue current practices"
            )

        return recommendations

    # Implementation of Sacred Codon abstract methods with immune integration

    def _execute_command_logic(self, command: SacredCommand) -> List[PollenEnvelope]:
        """Execute business logic with immune monitoring"""
        if command.command_type in [
            "create_greeting",
            "create_greeting_with_monitoring",
        ]:
            return self._create_greeting_logic(command)
        else:
            raise ValueError(f"Unknown command type: {command.command_type}")

    def _execute_query_logic(self, query_command: SacredCommand) -> Dict[str, Any]:
        """Execute query logic with immune status integration"""
        if query_command.command_type == "get_greeting_stats":
            # Include immune status in greeting stats
            basic_stats = {
                "aggregate_id": self.id,
                "greeting_count": self.greeting_count,
                "total_greetings_sent": len(self.greetings_sent),
                "status": self.status,
                "last_greeting": self.last_greeting,
                "sacred_compliance": self._calculate_compliance_score(),
                "codon_statistics": self.get_codon_statistics(),
            }

            # Add immune status
            basic_stats["immune_status"] = self.get_immune_status()

            return basic_stats
        else:
            return super()._execute_query_logic(query_command)

    def _execute_reaction_logic(
        self, event: PollenEnvelope, reaction_command: SacredCommand
    ) -> List[PollenEnvelope]:
        """Execute reaction logic with immune consideration"""
        if event.event_type in ["HelloHiveCreatedEvent", "GreetingReceivedEvent"]:
            return self._create_greeting_response_logic(event, reaction_command)
        elif event.event_type == "ImmuneMutationDetected":
            # React to immune system detected mutations
            return self._handle_immune_mutation_reaction(event, reaction_command)
        else:
            return []

    def _execute_immune_logic(
        self, mutation_event: PollenEnvelope, immune_command: SacredCommand
    ) -> List[Dict[str, Any]]:
        """Enhanced immune response logic for HelloHive"""
        corrective_actions = []

        payload_dict = dict(mutation_event.payload) if mutation_event.payload else {}

        if mutation_event.event_type == "ImmuneMutationDetected":
            mutation_details = payload_dict.get("mutation_details", {})
            mutation_type = mutation_details.get("mutation_type")

            if mutation_type == "temporal_anomaly":
                corrective_actions.append(
                    {
                        "action": "correct_temporal_anomaly",
                        "reason": "temporal_inconsistency_detected",
                        "correction": "synchronize_timestamps",
                        "severity": mutation_details.get("severity", 0.5),
                    }
                )

            elif mutation_type == "payload_contamination":
                corrective_actions.append(
                    {
                        "action": "quarantine_contaminated_payload",
                        "reason": "suspicious_content_detected",
                        "correction": "sanitize_and_validate",
                        "quarantine_required": True,
                    }
                )

            elif mutation_type == "event_malformation":
                corrective_actions.append(
                    {
                        "action": "reconstruct_malformed_event",
                        "reason": "structural_integrity_violation",
                        "correction": "validate_and_repair_structure",
                    }
                )

        # Record immune incident
        self.immune_incidents.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "mutation_type": mutation_event.event_type,
                "actions_taken": len(corrective_actions),
                "severity": payload_dict.get("severity", 0.0),
            }
        )

        return corrective_actions

    # Helper methods

    def _create_greeting_logic(self, command: SacredCommand) -> List[PollenEnvelope]:
        """Business logic for creating greetings with immune awareness"""
        greeting_data = command.payload

        # Validate greeting data (immune system will catch violations)
        if not greeting_data.get("message"):
            raise ValueError("Greeting message is required")

        # Update aggregate state
        self.greeting_count += 1
        self.last_greeting = greeting_data.get("message")
        self.greetings_sent.append(greeting_data)
        self.status = "active"

        # Create greeting event (will be processed by immune system)
        greeting_event = self._create_event(
            "HelloHiveCreatedEvent",
            {
                "message": greeting_data.get("message"),
                "sender": greeting_data.get("sender", "unknown"),
                "greeting_number": self.greeting_count,
                "command_id": command.command_id,
                "immune_monitored": True,
            },
        )

        return [greeting_event]

    def _handle_immune_mutation_reaction(
        self, mutation_event: PollenEnvelope, reaction_command: SacredCommand
    ) -> List[PollenEnvelope]:
        """Handle reactions to immune system mutation detections"""
        payload_dict = dict(mutation_event.payload)

        # Create acknowledgment event
        ack_event = self._create_event(
            "ImmuneMutationAcknowledged",
            {
                "original_mutation_event": mutation_event.event_id,
                "response_time": datetime.now(timezone.utc).isoformat(),
                "aggregate_response": "mutation_acknowledged",
                "health_check_initiated": True,
            },
        )

        # Optionally trigger self-diagnostic
        if payload_dict.get("severity", 0.0) > 0.8:
            diagnostic_event = self._create_event(
                "SelfDiagnosticTriggered",
                {
                    "trigger": "high_severity_mutation",
                    "diagnostic_type": "comprehensive_health_check",
                    "initiated_by": "immune_system",
                },
            )
            return [ack_event, diagnostic_event]

        return [ack_event]

    def _create_event(
        self, event_type: str, payload_data: Dict[str, Any]
    ) -> PollenEnvelope:
        """Helper to create PollenEnvelope events with immune-friendly structure"""
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


# Demonstration function
def demonstrate_immune_system_integration():
    """Demonstrate immune system integration with Sacred Codon patterns"""

    print("🧬🏥 Demonstrating Immune System Integration with Sacred Codons")
    print("=" * 80)

    # Create immune-enabled aggregate
    immune_aggregate = HelloHiveImmuneAggregate("hello-hive-immune-001")

    print(f"\n📊 Initial Health Report:")
    initial_health = immune_aggregate.get_comprehensive_health_report()
    print(f"   Health Score: {initial_health['health_score']:.2f}")
    print(f"   Recommendations: {initial_health['recommendations']}")

    # 1. Normal greeting creation (should be healthy)
    print(f"\n1. 🌟 Creating Normal Greeting (Sacred Codon + Immune Monitoring)")
    normal_events = immune_aggregate.create_greeting_with_immune_monitoring(
        {
            "message": "Hello, Sacred Hive with Immune Protection!",
            "sender": "Claude",
            "priority": "high",
        }
    )
    print(f"   Created {len(normal_events)} events successfully")

    # 2. Simulate various mutation types
    mutation_types = [
        "temporal_anomaly",
        "payload_contamination",
        "event_malformation",
        "protocol_drift",
    ]

    for mutation_type in mutation_types:
        print(
            f"\n2.{mutation_types.index(mutation_type) + 1} 🦠 Testing {mutation_type} Detection:"
        )
        immune_events = immune_aggregate.simulate_mutation_event(mutation_type)
        print(f"   Immune system generated {len(immune_events)} response events")

    # 3. Final health assessment
    print(f"\n📊 Final Health Assessment:")
    final_health = immune_aggregate.get_comprehensive_health_report()
    print(f"   Health Score: {final_health['health_score']:.2f}")
    print(
        f"   Sacred Compliance: {final_health['sacred_codon_compliance']['sacred_compliance']:.2f}"
    )
    print(
        f"   Mutations Detected: {final_health['immune_system_status']['mutations_detected']}"
    )
    print(f"   Immune Incidents: {len(immune_aggregate.immune_incidents)}")

    print(f"\n🏥 Immune System Statistics:")
    global_stats = final_health.get("global_immune_stats", {})
    if "total_mutations" in global_stats:
        print(f"   Total Mutations Detected: {global_stats['total_mutations']}")
        print(
            f"   Most Common Mutation: {global_stats.get('most_common_mutation', 'none')}"
        )
        print(f"   Immune Efficiency: {global_stats.get('immune_efficiency', 0.0):.2f}")

    print(f"\n💡 Health Recommendations:")
    for rec in final_health["recommendations"]:
        print(f"   • {rec}")

    print(f"\n✅ Immune System Integration Demonstration Complete")
    print(
        f"   The Hive's immune system successfully detected and responded to mutations"
    )
    print(f"   while maintaining Sacred Codon architectural integrity.")

    return immune_aggregate


if __name__ == "__main__":
    demonstrate_immune_system_integration()
