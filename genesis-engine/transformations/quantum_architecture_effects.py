#!/usr/bin/env python3
"""
⚛️ Quantum Architecture Effects System
Implements quantum mechanical principles for distributed software systems.

This module provides quantum-inspired behaviors for microservices and distributed architectures:
- Superposition: Services existing in multiple states simultaneously
- Entanglement: Instantaneous state correlation between services
- Coherence: Phase-synchronized system states
- Tunneling: Bypassing normal architectural barriers
- Uncertainty: Fundamental trade-offs in system observability
"""

import math
import random
import asyncio
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any, Set
from enum import Enum
from datetime import datetime


class QuantumState(Enum):
    """Quantum states for distributed system components"""

    SUPERPOSITION = "superposition"  # Multiple states simultaneously
    ENTANGLED = "entangled"  # Correlated with other services
    COHERENT = "coherent"  # Phase-synchronized
    DECOHERENT = "decoherent"  # Lost synchronization
    TUNNELING = "tunneling"  # Bypassing barriers
    GROUND = "ground"  # Lowest energy state
    EXCITED = "excited"  # Higher energy state
    MIXED = "mixed"  # Partially coherent state


class ObservableProperty(Enum):
    """Observable properties subject to quantum uncertainty"""

    PERFORMANCE = "performance"  # Response time, throughput
    AVAILABILITY = "availability"  # Uptime, reliability
    CONSISTENCY = "consistency"  # Data consistency level
    LOAD = "load"  # Resource utilization
    LATENCY = "latency"  # Network delay
    ERROR_RATE = "error_rate"  # Failure frequency
    RESOURCE_USAGE = "resource_usage"  # CPU, memory, disk


@dataclass
class QuantumAmplitude:
    """Complex amplitude representing quantum state probability"""

    real: float = 0.0
    imaginary: float = 0.0

    @property
    def magnitude_squared(self) -> float:
        """Calculate |ψ|² - probability of observing this state"""
        return self.real**2 + self.imaginary**2

    @property
    def phase(self) -> float:
        """Calculate phase angle in radians"""
        return math.atan2(self.imaginary, self.real)

    def normalize(self):
        """Normalize amplitude so |ψ|² = 1"""
        magnitude = math.sqrt(self.magnitude_squared)
        if magnitude > 0:
            self.real /= magnitude
            self.imaginary /= magnitude


@dataclass
class QuantumServiceState:
    """Quantum state representation for a microservice"""

    service_name: str
    amplitudes: Dict[str, QuantumAmplitude] = field(
        default_factory=dict
    )  # State -> Amplitude
    entangled_services: Set[str] = field(default_factory=set)
    coherence_time: float = 1000.0  # ms - how long coherence lasts
    last_observation: Optional[datetime] = None
    measurement_count: int = 0

    def __post_init__(self):
        """Initialize with ground state if no amplitudes provided"""
        if not self.amplitudes:
            self.amplitudes["ground"] = QuantumAmplitude(real=1.0, imaginary=0.0)

    def add_superposition_state(self, state_name: str, amplitude: QuantumAmplitude):
        """Add a state to the superposition"""
        self.amplitudes[state_name] = amplitude
        self._normalize_amplitudes()

    def _normalize_amplitudes(self):
        """Ensure total probability = 1"""
        total_prob = sum(amp.magnitude_squared for amp in self.amplitudes.values())
        if total_prob > 0:
            normalization = math.sqrt(1.0 / total_prob)
            for amp in self.amplitudes.values():
                amp.real *= normalization
                amp.imaginary *= normalization

    def get_state_probabilities(self) -> Dict[str, float]:
        """Get classical probabilities for each state"""
        return {state: amp.magnitude_squared for state, amp in self.amplitudes.items()}

    def measure_state(self) -> str:
        """Collapse superposition to a definite state (quantum measurement)"""
        probabilities = self.get_state_probabilities()
        states = list(probabilities.keys())
        weights = list(probabilities.values())

        # Quantum measurement collapses the state
        measured_state = random.choices(states, weights=weights)[0]

        # After measurement, service is in definite state
        self.amplitudes = {measured_state: QuantumAmplitude(real=1.0, imaginary=0.0)}
        self.last_observation = datetime.now()
        self.measurement_count += 1

        return measured_state

    def evolve_time(self, delta_time: float):
        """Evolve quantum state over time (Schrödinger evolution)"""
        # Simple phase evolution based on energy levels
        energy_levels = {
            "ground": 0.0,
            "excited": 1.0,
            "error": 2.0,
            "overloaded": 1.5,
            "idle": 0.5,
        }

        for state_name, amplitude in self.amplitudes.items():
            energy = energy_levels.get(state_name, 1.0)
            phase_shift = energy * delta_time * 0.001  # Scale factor

            # Apply phase evolution: |ψ⟩ → e^(-iEt/ℏ)|ψ⟩
            cos_phase = math.cos(phase_shift)
            sin_phase = math.sin(phase_shift)

            new_real = amplitude.real * cos_phase + amplitude.imaginary * sin_phase
            new_imaginary = amplitude.imaginary * cos_phase - amplitude.real * sin_phase

            amplitude.real = new_real
            amplitude.imaginary = new_imaginary

    def decohere(self, decoherence_rate: float = 0.01):
        """Gradually lose quantum coherence (environmental decoherence)"""
        if len(self.amplitudes) <= 1:
            return  # No coherence to lose

        # Random phase noise destroys coherence
        for amplitude in self.amplitudes.values():
            phase_noise = random.gauss(0, decoherence_rate)
            magnitude = math.sqrt(amplitude.magnitude_squared)
            current_phase = amplitude.phase

            new_phase = current_phase + phase_noise
            amplitude.real = magnitude * math.cos(new_phase)
            amplitude.imaginary = magnitude * math.sin(new_phase)


@dataclass
class EntanglementPair:
    """Represents quantum entanglement between two services"""

    service1: str
    service2: str
    correlation_strength: float  # -1 to 1 (negative = anti-correlated)
    entanglement_type: str  # "consistency", "performance", "availability"
    created_at: datetime = field(default_factory=datetime.now)
    decay_rate: float = 0.001  # How quickly entanglement decays

    def is_active(self) -> bool:
        """Check if entanglement is still active"""
        time_since_creation = (datetime.now() - self.created_at).total_seconds()
        decay_factor = math.exp(-self.decay_rate * time_since_creation)
        return decay_factor > 0.1  # 10% threshold

    def get_correlation_strength(self) -> float:
        """Get current correlation strength accounting for decay"""
        time_since_creation = (datetime.now() - self.created_at).total_seconds()
        decay_factor = math.exp(-self.decay_rate * time_since_creation)
        return self.correlation_strength * decay_factor


@dataclass
class QuantumTunnelingEvent:
    """Represents a quantum tunneling event bypassing normal barriers"""

    source_service: str
    target_service: str
    barrier_height: float  # Energy barrier to overcome
    tunneling_probability: float  # Probability of successful tunneling
    bypass_type: str  # "authentication", "rate_limiting", "circuit_breaker"
    timestamp: datetime = field(default_factory=datetime.now)

    def calculate_tunneling_probability(self, service_energy: float) -> float:
        """Calculate quantum tunneling probability using WKB approximation"""
        if service_energy >= self.barrier_height:
            return 1.0  # Classical case - enough energy to go over barrier

        # Quantum tunneling probability: P ≈ e^(-2√(2m(V-E))a/ℏ)
        # Simplified for architectural barriers
        barrier_difference = self.barrier_height - service_energy
        tunneling_factor = -2.0 * math.sqrt(barrier_difference)
        return math.exp(tunneling_factor)


class QuantumUncertaintyPrinciple:
    """Implements Heisenberg uncertainty principle for system observables"""

    # Uncertainty relationships between observables
    UNCERTAINTY_PAIRS = [
        (ObservableProperty.PERFORMANCE, ObservableProperty.CONSISTENCY),
        (ObservableProperty.AVAILABILITY, ObservableProperty.LATENCY),
        (ObservableProperty.LOAD, ObservableProperty.ERROR_RATE),
    ]

    @staticmethod
    def calculate_uncertainty(
        observable1: ObservableProperty,
        observable2: ObservableProperty,
        measurement_precision1: float,
        measurement_precision2: float,
    ) -> Tuple[float, float]:
        """Calculate uncertainty bounds based on complementary observables"""

        # Check if observables are complementary (non-commuting)
        is_complementary = any(
            {observable1, observable2} == {pair[0], pair[1]}
            for pair in QuantumUncertaintyPrinciple.UNCERTAINTY_PAIRS
        )

        if not is_complementary:
            return measurement_precision1, measurement_precision2

        # Apply uncertainty principle: ΔA·ΔB ≥ ℏ/2
        # For system observables, use architectural uncertainty constant
        planck_constant = 0.1  # Architectural uncertainty constant
        minimum_product = planck_constant / 2

        current_product = measurement_precision1 * measurement_precision2

        if current_product < minimum_product:
            # Need to increase uncertainties to satisfy principle
            scaling_factor = math.sqrt(minimum_product / current_product)
            return (
                measurement_precision1 * scaling_factor,
                measurement_precision2 * scaling_factor,
            )

        return measurement_precision1, measurement_precision2


class QuantumArchitectureOrchestrator:
    """Orchestrates quantum effects across distributed architecture"""

    def __init__(self):
        self.quantum_services: Dict[str, QuantumServiceState] = {}
        self.entanglements: List[EntanglementPair] = []
        self.tunneling_events: List[QuantumTunnelingEvent] = []
        self.coherence_groups: Dict[str, Set[str]] = {}  # Coherent service groups
        self.uncertainty_calculator = QuantumUncertaintyPrinciple()

        # Quantum evolution parameters
        self.evolution_interval = 100  # ms
        self.decoherence_rate = 0.01
        self.last_evolution_time = datetime.now()

    def register_quantum_service(
        self,
        service_name: str,
        initial_state: Optional[Dict[str, QuantumAmplitude]] = None,
    ) -> QuantumServiceState:
        """Register a service for quantum effects"""
        quantum_state = QuantumServiceState(
            service_name=service_name,
            amplitudes=initial_state or {},
            coherence_time=1000.0,
        )
        self.quantum_services[service_name] = quantum_state
        return quantum_state

    def create_superposition(
        self, service_name: str, states: Dict[str, Tuple[float, float]]
    ):
        """Create quantum superposition of service states"""
        if service_name not in self.quantum_services:
            self.register_quantum_service(service_name)

        service = self.quantum_services[service_name]
        service.amplitudes.clear()

        for state_name, (real, imaginary) in states.items():
            amplitude = QuantumAmplitude(real=real, imaginary=imaginary)
            service.amplitudes[state_name] = amplitude

        service._normalize_amplitudes()
        print(f"⚛️ Created superposition for {service_name}: {list(states.keys())}")

    def entangle_services(
        self,
        service1: str,
        service2: str,
        correlation_strength: float,
        entanglement_type: str = "consistency",
    ):
        """Create quantum entanglement between two services"""

        # Register services if not already registered
        if service1 not in self.quantum_services:
            self.register_quantum_service(service1)
        if service2 not in self.quantum_services:
            self.register_quantum_service(service2)

        # Create entanglement pair
        entanglement = EntanglementPair(
            service1=service1,
            service2=service2,
            correlation_strength=correlation_strength,
            entanglement_type=entanglement_type,
        )
        self.entanglements.append(entanglement)

        # Update service entanglement records
        self.quantum_services[service1].entangled_services.add(service2)
        self.quantum_services[service2].entangled_services.add(service1)

        print(
            f"🔗 Entangled {service1} ↔ {service2} (strength: {correlation_strength:.2f})"
        )

    def measure_service_state(self, service_name: str) -> str:
        """Perform quantum measurement on service, collapsing superposition"""
        if service_name not in self.quantum_services:
            return "unknown"

        service = self.quantum_services[service_name]
        measured_state = service.measure_state()

        # Handle entanglement collapse
        self._propagate_entanglement_collapse(service_name, measured_state)

        print(f"📊 Measured {service_name}: {measured_state}")
        return measured_state

    def _propagate_entanglement_collapse(
        self, measured_service: str, measured_state: str
    ):
        """Propagate measurement collapse to entangled services"""
        for entanglement in self.entanglements:
            if not entanglement.is_active():
                continue

            entangled_service = None
            if entanglement.service1 == measured_service:
                entangled_service = entanglement.service2
            elif entanglement.service2 == measured_service:
                entangled_service = entanglement.service1

            if entangled_service and entangled_service in self.quantum_services:
                correlation = entanglement.get_correlation_strength()
                self._apply_entanglement_correlation(
                    entangled_service,
                    measured_state,
                    correlation,
                    entanglement.entanglement_type,
                )

    def _apply_entanglement_correlation(
        self,
        service_name: str,
        correlated_state: str,
        correlation_strength: float,
        entanglement_type: str,
    ):
        """Apply entanglement correlation to collapse entangled service state"""
        service = self.quantum_services[service_name]

        # Strong positive correlation -> same state
        if correlation_strength > 0.7:
            if correlated_state in service.amplitudes:
                service.amplitudes = {
                    correlated_state: QuantumAmplitude(real=1.0, imaginary=0.0)
                }
                print(
                    f"🔗 {service_name} collapsed to {correlated_state} (entanglement)"
                )

        # Strong negative correlation -> opposite state
        elif correlation_strength < -0.7:
            opposite_states = {
                "ground": "excited",
                "excited": "ground",
                "healthy": "error",
                "error": "healthy",
                "low_load": "high_load",
                "high_load": "low_load",
            }
            opposite_state = opposite_states.get(correlated_state, "ground")
            if opposite_state in service.amplitudes:
                service.amplitudes = {
                    opposite_state: QuantumAmplitude(real=1.0, imaginary=0.0)
                }
                print(
                    f"🔗 {service_name} anti-collapsed to {opposite_state} (entanglement)"
                )

    def attempt_quantum_tunneling(
        self,
        source_service: str,
        target_service: str,
        barrier_type: str,
        service_energy: float,
    ) -> bool:
        """Attempt quantum tunneling to bypass architectural barriers"""

        barrier_heights = {
            "authentication": 2.0,
            "rate_limiting": 1.5,
            "circuit_breaker": 2.5,
            "load_balancer": 1.0,
            "firewall": 3.0,
        }

        barrier_height = barrier_heights.get(barrier_type, 2.0)

        tunneling_event = QuantumTunnelingEvent(
            source_service=source_service,
            target_service=target_service,
            barrier_height=barrier_height,
            tunneling_probability=0.0,
            bypass_type=barrier_type,
        )

        tunneling_prob = tunneling_event.calculate_tunneling_probability(service_energy)
        tunneling_event.tunneling_probability = tunneling_prob

        success = random.random() < tunneling_prob

        if success:
            print(
                f"🌊 Quantum tunneling successful: {source_service} → {target_service} "
                f"(bypassed {barrier_type}, prob: {tunneling_prob:.3f})"
            )
        else:
            print(
                f"🚫 Quantum tunneling failed: {source_service} → {target_service} "
                f"(blocked by {barrier_type}, prob: {tunneling_prob:.3f})"
            )

        self.tunneling_events.append(tunneling_event)
        return success

    def create_coherent_group(self, group_name: str, service_names: List[str]):
        """Create a coherent group of services that maintain phase synchronization"""
        self.coherence_groups[group_name] = set(service_names)

        # Synchronize phases of all services in group
        if service_names:
            reference_service = self.quantum_services.get(service_names[0])
            if reference_service:
                reference_phase = list(reference_service.amplitudes.values())[0].phase

                for service_name in service_names[1:]:
                    if service_name in self.quantum_services:
                        service = self.quantum_services[service_name]
                        for amplitude in service.amplitudes.values():
                            magnitude = math.sqrt(amplitude.magnitude_squared)
                            amplitude.real = magnitude * math.cos(reference_phase)
                            amplitude.imaginary = magnitude * math.sin(reference_phase)

        print(f"🌊 Created coherent group '{group_name}': {service_names}")

    def evolve_quantum_system(self, delta_time: float):
        """Evolve the entire quantum system over time"""

        # Evolve individual service states
        for service in self.quantum_services.values():
            service.evolve_time(delta_time)
            service.decohere(self.decoherence_rate)

        # Maintain coherence within groups
        for group_name, service_names in self.coherence_groups.items():
            self._maintain_group_coherence(service_names)

        # Clean up expired entanglements
        self.entanglements = [e for e in self.entanglements if e.is_active()]

        # Clean up old tunneling events (keep last 100)
        if len(self.tunneling_events) > 100:
            self.tunneling_events = self.tunneling_events[-100:]

    def _maintain_group_coherence(self, service_names: Set[str]):
        """Maintain phase coherence within a service group"""
        active_services = [
            name for name in service_names if name in self.quantum_services
        ]
        if len(active_services) < 2:
            return

        # Calculate average phase
        phases = []
        for service_name in active_services:
            service = self.quantum_services[service_name]
            for amplitude in service.amplitudes.values():
                phases.append(amplitude.phase)

        if phases:
            avg_phase = sum(phases) / len(phases)

            # Adjust all services toward average phase
            for service_name in active_services:
                service = self.quantum_services[service_name]
                for amplitude in service.amplitudes.values():
                    magnitude = math.sqrt(amplitude.magnitude_squared)
                    # Partially align with average phase (gradual coherence)
                    current_phase = amplitude.phase
                    aligned_phase = current_phase * 0.9 + avg_phase * 0.1
                    amplitude.real = magnitude * math.cos(aligned_phase)
                    amplitude.imaginary = magnitude * math.sin(aligned_phase)

    def get_system_quantum_state(self) -> Dict[str, Any]:
        """Get comprehensive quantum state of the entire system"""
        return {
            "services": {
                name: {
                    "state_probabilities": service.get_state_probabilities(),
                    "entangled_with": list(service.entangled_services),
                    "measurement_count": service.measurement_count,
                    "last_observation": service.last_observation.isoformat()
                    if service.last_observation
                    else None,
                }
                for name, service in self.quantum_services.items()
            },
            "active_entanglements": [
                {
                    "services": [e.service1, e.service2],
                    "strength": e.get_correlation_strength(),
                    "type": e.entanglement_type,
                    "age_seconds": (datetime.now() - e.created_at).total_seconds(),
                }
                for e in self.entanglements
                if e.is_active()
            ],
            "coherent_groups": {
                name: list(services) for name, services in self.coherence_groups.items()
            },
            "recent_tunneling_events": [
                {
                    "source": event.source_service,
                    "target": event.target_service,
                    "barrier": event.bypass_type,
                    "probability": event.tunneling_probability,
                    "timestamp": event.timestamp.isoformat(),
                }
                for event in self.tunneling_events[-10:]  # Last 10 events
            ],
            "system_metrics": {
                "total_services": len(self.quantum_services),
                "superposition_services": len(
                    [s for s in self.quantum_services.values() if len(s.amplitudes) > 1]
                ),
                "entangled_pairs": len(self.entanglements),
                "coherent_groups": len(self.coherence_groups),
                "tunneling_events": len(self.tunneling_events),
            },
        }


# Example usage and demonstration
async def demonstrate_quantum_architecture():
    """Demonstrate quantum effects in distributed architecture"""
    print("⚛️ Quantum Architecture Effects - Demonstration")
    print("=" * 60)

    orchestrator = QuantumArchitectureOrchestrator()

    # Register services and create superposition states
    print("\n🔬 Creating quantum superposition states...")

    # API Gateway in superposition of load states
    orchestrator.create_superposition(
        "api-gateway",
        {
            "low_load": (0.7, 0.1),  # 70% probability, small imaginary component
            "medium_load": (0.5, 0.3),  # 50% + imaginary
            "high_load": (0.2, 0.1),  # 20% probability
        },
    )

    # Database in superposition of consistency states
    orchestrator.create_superposition(
        "database",
        {
            "strong_consistency": (0.8, 0.0),
            "eventual_consistency": (0.4, 0.2),
            "weak_consistency": (0.3, 0.1),
        },
    )

    # Create entanglement between services
    print("\n🔗 Creating quantum entanglements...")
    orchestrator.entangle_services(
        "api-gateway",
        "database",
        correlation_strength=0.85,
        entanglement_type="consistency",
    )

    orchestrator.entangle_services(
        "auth-service",
        "user-service",
        correlation_strength=-0.7,  # Anti-correlation
        entanglement_type="availability",
    )

    # Create coherent service group
    print("\n🌊 Creating coherent service groups...")
    orchestrator.create_coherent_group(
        "payment_cluster", ["payment-service", "billing-service", "invoice-service"]
    )

    # Demonstrate quantum tunneling
    print("\n🌊 Attempting quantum tunneling...")
    success1 = orchestrator.attempt_quantum_tunneling(
        "external-client", "secure-api", "authentication", service_energy=1.0
    )

    success2 = orchestrator.attempt_quantum_tunneling(
        "batch-processor", "rate-limited-api", "rate_limiting", service_energy=2.0
    )

    # Evolve system over time
    print("\n⏱️ Evolving quantum system...")
    for i in range(3):
        await asyncio.sleep(0.1)  # Small delay for demonstration
        orchestrator.evolve_quantum_system(delta_time=100.0)  # 100ms evolution
        print(f"   Evolution step {i + 1} completed")

    # Perform measurements (collapses superposition)
    print("\n📊 Performing quantum measurements...")
    api_state = orchestrator.measure_service_state("api-gateway")
    db_state = orchestrator.measure_service_state("database")

    # Show final system state
    print("\n📈 Final quantum system state:")
    system_state = orchestrator.get_system_quantum_state()

    print(f"   Total services: {system_state['system_metrics']['total_services']}")
    print(
        f"   Services in superposition: {system_state['system_metrics']['superposition_services']}"
    )
    print(f"   Active entanglements: {len(system_state['active_entanglements'])}")
    print(f"   Tunneling events: {system_state['system_metrics']['tunneling_events']}")

    print("\n⚛️ Quantum architecture demonstration complete!")
    return system_state


if __name__ == "__main__":
    # Run demonstration
    asyncio.run(demonstrate_quantum_architecture())
