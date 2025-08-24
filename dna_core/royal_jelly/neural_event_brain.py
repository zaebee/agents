"""
Hive Neural Network Event Processing Engine - Bio/Sci Brain Architecture

This module implements a brain-like neural network system for event processing
that follows bio/sci nature/orgs philosophy. Events are processed through
interconnected neural networks that learn, adapt, and form synaptic connections.

Key Bio/Sci Principles:
- Neural networks are born and evolve naturally
- Synaptic connections form based on beneficial relationships
- Learning happens through repetition and reinforcement
- Brain regions specialize in different event types
- Memory formation follows organic patterns
- Collective neural intelligence emerges
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid
import math
import random
from datetime import datetime, timezone
from collections import defaultdict, deque
import threading
from concurrent.futures import ThreadPoolExecutor

# Flexible event handling - can work with PollenEnvelope or mock objects
try:
    from google.protobuf.struct_pb2 import Struct
    from google.protobuf.timestamp_pb2 import Timestamp
    from dna_core.pollen_protocol_pb2 import PollenEnvelope

    PROTOBUF_AVAILABLE = True
except ImportError:
    PROTOBUF_AVAILABLE = False
    PollenEnvelope = Any  # Fallback for type hints
from .sacred_codon import (
    SacredCommand,
    SacredCodonType,
    create_sacred_command,
)
from .immune_event_processor import (
    HiveAdaptationEngine,
)


class NeuronType(Enum):
    """Types of neurons in the Hive Neural Network - specialized like brain regions"""

    INPUT_SENSORY = "input_sensory"  # Sensory input processing
    PATTERN_RECOGNITION = "pattern_recognition"  # Pattern detection and analysis
    MEMORY_FORMATION = "memory_formation"  # Memory creation and storage
    DECISION_MAKING = "decision_making"  # Executive decision neurons
    MOTOR_OUTPUT = "motor_output"  # Action generation
    ASSOCIATION = "association"  # Cross-pattern association
    INHIBITORY = "inhibitory"  # Regulatory and control
    MIRROR = "mirror"  # Empathy and mimicry
    REWARD = "reward"  # Reinforcement learning
    TEMPORAL = "temporal"  # Time-based pattern processing


class ActivationFunction(Enum):
    """Neural activation functions - organic response patterns"""

    SIGMOID = "sigmoid"  # Smooth organic activation
    TANH = "tanh"  # Bipolar organic response
    RELU = "relu"  # Natural threshold activation
    LEAKY_RELU = "leaky_relu"  # Adaptive threshold
    SOFTMAX = "softmax"  # Probability distribution
    LINEAR = "linear"  # Direct transmission
    ORGANIC = "organic"  # Custom bio-inspired function


@dataclass
class SynapticConnection:
    """Represents a synaptic connection between neurons"""

    connection_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    pre_neuron_id: str = ""
    post_neuron_id: str = ""
    weight: float = 0.0
    strength: float = 1.0  # Connection strength (0.0 to 1.0)
    formation_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_activation: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    activation_count: int = 0
    plasticity: float = 0.1  # Learning rate for this connection
    is_inhibitory: bool = False
    neurotransmitter_type: str = "dopamine"  # Default reward neurotransmitter


@dataclass
class Neuron:
    """Individual neuron in the Hive Neural Network"""

    neuron_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    neuron_type: NeuronType = NeuronType.ASSOCIATION
    activation_function: ActivationFunction = ActivationFunction.SIGMOID
    threshold: float = 0.5
    bias: float = 0.0
    current_activation: float = 0.0
    previous_activation: float = 0.0

    # Bio/Sci properties
    birth_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    energy_level: float = 1.0
    stress_level: float = 0.0
    learning_rate: float = 0.01
    specialization_score: float = 0.0

    # Connections
    input_connections: List[SynapticConnection] = field(default_factory=list)
    output_connections: List[SynapticConnection] = field(default_factory=list)

    # Memory and adaptation
    activation_history: deque = field(default_factory=lambda: deque(maxlen=100))
    learned_patterns: Dict[str, float] = field(default_factory=dict)

    def activate(self, input_signal: float) -> float:
        """Activate the neuron with organic response patterns"""

        # Apply bias and threshold
        weighted_input = input_signal + self.bias

        # Calculate activation based on function type
        if self.activation_function == ActivationFunction.SIGMOID:
            activation = 1.0 / (1.0 + math.exp(-weighted_input))
        elif self.activation_function == ActivationFunction.TANH:
            activation = math.tanh(weighted_input)
        elif self.activation_function == ActivationFunction.RELU:
            activation = max(0.0, weighted_input)
        elif self.activation_function == ActivationFunction.LEAKY_RELU:
            activation = max(0.01 * weighted_input, weighted_input)
        elif self.activation_function == ActivationFunction.LINEAR:
            activation = weighted_input
        elif self.activation_function == ActivationFunction.ORGANIC:
            # Custom bio-inspired activation with energy and stress factors
            base_activation = 1.0 / (1.0 + math.exp(-weighted_input))
            energy_modifier = self.energy_level * 0.2 + 0.8
            stress_modifier = max(0.1, 1.0 - self.stress_level * 0.5)
            activation = base_activation * energy_modifier * stress_modifier
        else:
            activation = weighted_input

        # Apply threshold
        if activation < self.threshold:
            activation = 0.0

        # Update neuron state
        self.previous_activation = self.current_activation
        self.current_activation = activation
        self.activation_history.append(activation)

        # Update energy and stress based on activation
        self._update_biological_state(activation)

        return activation

    def _update_biological_state(self, activation: float):
        """Update biological properties based on activation"""

        # Energy consumption and recovery
        energy_consumption = activation * 0.01
        energy_recovery = 0.005
        self.energy_level = max(
            0.1, min(1.0, self.energy_level - energy_consumption + energy_recovery)
        )

        # Stress adaptation
        if activation > 0.8:
            self.stress_level = min(1.0, self.stress_level + 0.01)
        else:
            self.stress_level = max(0.0, self.stress_level - 0.005)

        # Learning rate adaptation
        if self.stress_level > 0.5:
            self.learning_rate = min(0.1, self.learning_rate * 1.01)
        else:
            self.learning_rate = max(0.001, self.learning_rate * 0.999)


@dataclass
class NeuralRegion:
    """Brain region containing specialized neurons"""

    region_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    region_name: str = ""
    specialized_function: str = ""
    neurons: List[Neuron] = field(default_factory=list)

    # Bio/Sci properties
    formation_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    maturity_level: float = 0.0  # 0.0 to 1.0
    plasticity: float = 1.0  # Ability to form new connections
    specialization_strength: float = 0.0

    # Regional characteristics
    excitability: float = 0.5
    inhibition_threshold: float = 0.7
    cooperation_factor: float = 0.8

    def process_regional_pattern(self, input_patterns: List[float]) -> List[float]:
        """Process patterns through the neural region"""

        if not self.neurons or not input_patterns:
            return []

        # Distribute inputs across neurons in the region
        outputs = []
        for i, neuron in enumerate(self.neurons):
            if i < len(input_patterns):
                activation = neuron.activate(input_patterns[i])
                outputs.append(activation)

        # Apply regional modulation
        modulated_outputs = []
        for output in outputs:
            # Apply regional excitability
            modulated = output * self.excitability

            # Apply cooperation factor for regional coherence
            if len(outputs) > 1:
                avg_output = sum(outputs) / len(outputs)
                modulated = (modulated + avg_output * self.cooperation_factor) / (
                    1 + self.cooperation_factor
                )

            modulated_outputs.append(modulated)

        # Update regional maturity
        self._update_regional_maturity(outputs)

        return modulated_outputs

    def _update_regional_maturity(self, activations: List[float]):
        """Update regional maturity based on activation patterns"""

        if not activations:
            return

        # Calculate activation coherence
        avg_activation = sum(activations) / len(activations)
        coherence = 1.0 - sum(abs(a - avg_activation) for a in activations) / len(
            activations
        )

        # Update maturity based on coherent activation
        maturity_increase = coherence * 0.001
        self.maturity_level = min(1.0, self.maturity_level + maturity_increase)

        # Update specialization based on consistent patterns
        if avg_activation > 0.6:
            self.specialization_strength = min(
                1.0, self.specialization_strength + 0.001
            )


class HiveNeuralEventBrain:
    """
    Bio/Sci Neural Network Event Processing Engine

    This system processes events through interconnected neural networks that
    learn and adapt like a biological brain. Neural regions specialize in
    different aspects of event processing, forming synaptic connections
    based on beneficial relationships.
    """

    def __init__(self, brain_name: str = "HiveEventBrain"):
        self.brain_id = str(uuid.uuid4())
        self.brain_name = brain_name
        self.birth_time = datetime.now(timezone.utc)

        # Neural architecture
        self.neural_regions: Dict[str, NeuralRegion] = {}
        self.all_neurons: Dict[str, Neuron] = {}
        self.synaptic_connections: Dict[str, SynapticConnection] = {}

        # Learning and memory
        self.event_memory: deque = deque(maxlen=1000)
        self.pattern_library: Dict[str, List[float]] = {}
        self.learned_associations: Dict[str, Dict[str, float]] = defaultdict(dict)

        # Bio/Sci brain state
        self.consciousness_level: float = 0.1
        self.attention_focus: Optional[str] = None
        self.emotional_state: Dict[str, float] = {
            "curiosity": 0.5,
            "satisfaction": 0.5,
            "stress": 0.0,
            "excitement": 0.3,
        }

        # Integration with existing systems
        self.adaptation_engine = HiveAdaptationEngine()

        # Threading for concurrent processing
        self._processing_lock = threading.RLock()
        self._thread_pool = ThreadPoolExecutor(max_workers=4)

        # Initialize brain structure
        self._initialize_brain_regions()
        self._create_initial_neural_pathways()

    def _initialize_brain_regions(self):
        """Create specialized brain regions like a biological brain"""

        # Sensory Input Region - processes incoming events
        sensory_region = NeuralRegion(
            region_name="SensoryInputCortex",
            specialized_function="Event input processing and initial pattern recognition",
            excitability=0.8,
            cooperation_factor=0.6,
        )

        # Create sensory neurons
        for i in range(10):
            neuron = Neuron(
                neuron_type=NeuronType.INPUT_SENSORY,
                activation_function=ActivationFunction.ORGANIC,
                threshold=0.3,
                learning_rate=0.02,
            )
            sensory_region.neurons.append(neuron)
            self.all_neurons[neuron.neuron_id] = neuron

        self.neural_regions["sensory"] = sensory_region

        # Pattern Recognition Region - analyzes event patterns
        pattern_region = NeuralRegion(
            region_name="PatternRecognitionCortex",
            specialized_function="Event pattern analysis and classification",
            excitability=0.6,
            cooperation_factor=0.8,
        )

        for i in range(15):
            neuron = Neuron(
                neuron_type=NeuronType.PATTERN_RECOGNITION,
                activation_function=ActivationFunction.SIGMOID,
                threshold=0.4,
                learning_rate=0.015,
            )
            pattern_region.neurons.append(neuron)
            self.all_neurons[neuron.neuron_id] = neuron

        self.neural_regions["pattern"] = pattern_region

        # Memory Formation Region - creates and stores memories
        memory_region = NeuralRegion(
            region_name="HippocampusAnalog",
            specialized_function="Event memory formation and retrieval",
            excitability=0.4,
            cooperation_factor=0.9,
        )

        for i in range(8):
            neuron = Neuron(
                neuron_type=NeuronType.MEMORY_FORMATION,
                activation_function=ActivationFunction.TANH,
                threshold=0.5,
                learning_rate=0.01,
            )
            memory_region.neurons.append(neuron)
            self.all_neurons[neuron.neuron_id] = neuron

        self.neural_regions["memory"] = memory_region

        # Decision Making Region - executive decisions
        executive_region = NeuralRegion(
            region_name="PrefrontalCortexAnalog",
            specialized_function="Event processing decisions and action planning",
            excitability=0.5,
            cooperation_factor=0.7,
        )

        for i in range(12):
            neuron = Neuron(
                neuron_type=NeuronType.DECISION_MAKING,
                activation_function=ActivationFunction.RELU,
                threshold=0.6,
                learning_rate=0.012,
            )
            executive_region.neurons.append(neuron)
            self.all_neurons[neuron.neuron_id] = neuron

        self.neural_regions["executive"] = executive_region

        # Motor Output Region - generates responses
        motor_region = NeuralRegion(
            region_name="MotorCortexAnalog",
            specialized_function="Sacred command generation and event responses",
            excitability=0.7,
            cooperation_factor=0.5,
        )

        for i in range(6):
            neuron = Neuron(
                neuron_type=NeuronType.MOTOR_OUTPUT,
                activation_function=ActivationFunction.LEAKY_RELU,
                threshold=0.4,
                learning_rate=0.008,
            )
            motor_region.neurons.append(neuron)
            self.all_neurons[neuron.neuron_id] = neuron

        self.neural_regions["motor"] = motor_region

        # Reward System - reinforcement learning
        reward_region = NeuralRegion(
            region_name="RewardSystemAnalog",
            specialized_function="Reinforcement learning and pattern value assessment",
            excitability=0.9,
            cooperation_factor=0.4,
        )

        for i in range(4):
            neuron = Neuron(
                neuron_type=NeuronType.REWARD,
                activation_function=ActivationFunction.ORGANIC,
                threshold=0.3,
                learning_rate=0.025,
            )
            reward_region.neurons.append(neuron)
            self.all_neurons[neuron.neuron_id] = neuron

        self.neural_regions["reward"] = reward_region

    def _create_initial_neural_pathways(self):
        """Create initial synaptic connections between brain regions"""

        # Sensory -> Pattern Recognition pathway
        self._create_region_connections("sensory", "pattern", 0.3, 0.7)

        # Pattern -> Memory pathway
        self._create_region_connections("pattern", "memory", 0.2, 0.6)

        # Pattern -> Executive pathway
        self._create_region_connections("pattern", "executive", 0.4, 0.8)

        # Memory -> Executive pathway
        self._create_region_connections("memory", "executive", 0.3, 0.7)

        # Executive -> Motor pathway
        self._create_region_connections("executive", "motor", 0.5, 0.9)

        # Reward feedback pathways
        self._create_region_connections("motor", "reward", 0.2, 0.5)
        self._create_region_connections("reward", "pattern", 0.1, 0.4)
        self._create_region_connections("reward", "executive", 0.2, 0.6)

    def _create_region_connections(
        self, from_region: str, to_region: str, min_weight: float, max_weight: float
    ):
        """Create synaptic connections between neural regions"""

        from_neurons = self.neural_regions[from_region].neurons
        to_neurons = self.neural_regions[to_region].neurons

        # Create connections with some randomness for diversity
        connection_probability = 0.3  # 30% connection rate

        for from_neuron in from_neurons:
            for to_neuron in to_neurons:
                if random.random() < connection_probability:
                    weight = random.uniform(min_weight, max_weight)

                    connection = SynapticConnection(
                        pre_neuron_id=from_neuron.neuron_id,
                        post_neuron_id=to_neuron.neuron_id,
                        weight=weight,
                        strength=random.uniform(0.5, 1.0),
                        plasticity=random.uniform(0.05, 0.15),
                    )

                    # Add to neuron connections
                    from_neuron.output_connections.append(connection)
                    to_neuron.input_connections.append(connection)

                    # Store in brain's connection map
                    self.synaptic_connections[connection.connection_id] = connection

    def process_event_through_neural_network(self, event: Any) -> List[SacredCommand]:
        """
        Process an event through the neural network brain

        This is the main processing pipeline that flows like neural signal processing
        """

        with self._processing_lock:
            try:
                # Step 1: Convert event to neural input signals
                input_signals = self._encode_event_to_neural_signals(event)

                # Step 2: Process through sensory region
                sensory_outputs = self.neural_regions[
                    "sensory"
                ].process_regional_pattern(input_signals)

                # Step 3: Pattern recognition processing
                pattern_outputs = self._propagate_signals(
                    "sensory", "pattern", sensory_outputs
                )

                # Step 4: Memory formation and retrieval
                memory_outputs = self._propagate_signals(
                    "pattern", "memory", pattern_outputs
                )
                self._form_event_memory(event, pattern_outputs, memory_outputs)

                # Step 5: Executive decision making
                executive_inputs = pattern_outputs + memory_outputs
                executive_outputs = self.neural_regions[
                    "executive"
                ].process_regional_pattern(executive_inputs)

                # Step 6: Motor command generation
                motor_outputs = self._propagate_signals(
                    "executive", "motor", executive_outputs
                )
                sacred_commands = self._generate_sacred_commands_from_neural_outputs(
                    event, motor_outputs
                )

                # Step 7: Reward processing and learning
                reward_signals = self._calculate_reward_signals(event, sacred_commands)
                self._process_reward_learning(reward_signals)

                # Step 8: Update consciousness and attention
                self._update_consciousness_state(pattern_outputs, executive_outputs)

                # Step 9: Store event in memory
                self.event_memory.append(
                    {
                        "event": event,
                        "processing_time": datetime.now(timezone.utc),
                        "neural_response": sacred_commands,
                        "consciousness_level": self.consciousness_level,
                    }
                )

                return sacred_commands

            except Exception as e:
                # Neural processing error - create adaptive response
                return self._handle_neural_processing_error(event, str(e))

    def _encode_event_to_neural_signals(self, event: Any) -> List[float]:
        """Convert event object to neural input signals"""

        signals = []

        # Event type encoding
        event_type = getattr(event, "event_type", "unknown")
        event_type_hash = hash(event_type) % 1000 / 1000.0
        signals.append(event_type_hash)

        # Temporal encoding
        timestamp = getattr(event, "timestamp", None)
        if timestamp:
            if hasattr(timestamp, "seconds"):  # Protobuf timestamp
                time_signal = (timestamp.seconds % 3600) / 3600.0
            else:  # Regular datetime
                time_signal = (timestamp.timestamp() % 3600) / 3600.0
            signals.append(time_signal)
        else:
            signals.append(0.5)

        # Aggregate ID encoding
        aggregate_id = getattr(event, "aggregate_id", None)
        if aggregate_id:
            aggregate_hash = hash(aggregate_id) % 1000 / 1000.0
            signals.append(aggregate_hash)
        else:
            signals.append(0.0)

        # Payload complexity encoding
        payload = getattr(event, "payload", {})
        payload_complexity = len(str(payload)) / 1000.0
        signals.append(min(1.0, payload_complexity))

        # Event version encoding
        event_version = getattr(event, "event_version", "1.0")
        try:
            version_signal = float(event_version) / 10.0
        except:
            version_signal = 0.1
        signals.append(version_signal)

        # Event ID uniqueness
        event_id = getattr(event, "event_id", None)
        if event_id:
            id_uniqueness = (hash(event_id) % 100) / 100.0
            signals.append(id_uniqueness)
        else:
            signals.append(0.0)

        # Pad or truncate to expected input size
        target_size = len(self.neural_regions["sensory"].neurons)
        while len(signals) < target_size:
            signals.append(random.uniform(0.0, 0.1))

        return signals[:target_size]

    def _propagate_signals(
        self, from_region: str, to_region: str, input_signals: List[float]
    ) -> List[float]:
        """Propagate neural signals between brain regions"""

        from_neurons = self.neural_regions[from_region].neurons
        to_neurons = self.neural_regions[to_region].neurons

        # Initialize output signals
        output_signals = [0.0] * len(to_neurons)

        # Process each connection
        for i, from_neuron in enumerate(from_neurons):
            if i < len(input_signals):
                from_activation = input_signals[i]

                for connection in from_neuron.output_connections:
                    # Find target neuron
                    for j, to_neuron in enumerate(to_neurons):
                        if to_neuron.neuron_id == connection.post_neuron_id:
                            # Apply synaptic transmission
                            signal_strength = (
                                from_activation
                                * connection.weight
                                * connection.strength
                            )
                            output_signals[j] += signal_strength

                            # Update connection based on usage
                            connection.last_activation = datetime.now(timezone.utc)
                            connection.activation_count += 1

                            # Hebbian learning: strengthen active connections
                            if from_activation > 0.5 and signal_strength > 0.3:
                                connection.weight = min(
                                    1.0,
                                    connection.weight + connection.plasticity * 0.01,
                                )

                            break

        # Process through target region
        return self.neural_regions[to_region].process_regional_pattern(output_signals)

    def _form_event_memory(
        self, event: Any, pattern_signals: List[float], memory_signals: List[float]
    ):
        """Form memory patterns from event processing"""

        # Create pattern signature
        event_type = getattr(event, "event_type", "unknown")
        pattern_key = f"{event_type}_{len(pattern_signals)}"

        # Store in pattern library
        if pattern_key not in self.pattern_library:
            self.pattern_library[pattern_key] = pattern_signals.copy()
        else:
            # Update existing pattern with weighted average
            existing = self.pattern_library[pattern_key]
            for i in range(min(len(existing), len(pattern_signals))):
                existing[i] = existing[i] * 0.9 + pattern_signals[i] * 0.1

        # Create associative memory
        aggregate_id = getattr(event, "aggregate_id", None)
        if aggregate_id:
            self.learned_associations[event_type][aggregate_id] = sum(
                memory_signals
            ) / len(memory_signals)

    def _generate_sacred_commands_from_neural_outputs(
        self, event: Any, motor_outputs: List[float]
    ) -> List[SacredCommand]:
        """Convert neural motor outputs to Sacred Commands"""

        commands = []

        # Threshold for command generation
        command_threshold = 0.6

        # Process each motor output
        for i, output in enumerate(motor_outputs):
            if output > command_threshold:
                # Determine command type based on neural activation pattern
                if output > 0.8:
                    command_type = "neural_high_priority_response"
                elif output > 0.7:
                    command_type = "neural_pattern_learned"
                else:
                    command_type = "neural_adaptive_response"

                # Create Sacred Command
                event_type = getattr(event, "event_type", "unknown")
                command = create_sacred_command(
                    command_type=command_type,
                    payload={
                        "neural_motor_index": i,
                        "activation_strength": output,
                        "source_event_type": event_type,
                        "consciousness_level": self.consciousness_level,
                        "neural_pattern_confidence": output,
                        "brain_region": "motor",
                        "synaptic_efficiency": self._calculate_synaptic_efficiency(),
                        "emotional_context": self.emotional_state.copy(),
                        "attention_focus": self.attention_focus,
                    },
                    codon_type=SacredCodonType.NEURAL_RESPONSE,
                    source=f"hive_neural_brain_{self.brain_id}",
                )
                commands.append(command)

        # If no commands generated, create a minimal observation command
        if not commands:
            event_type = getattr(event, "event_type", "unknown")
            observation_command = create_sacred_command(
                command_type="neural_passive_observation",
                payload={
                    "event_observed": event_type,
                    "neural_state": "monitoring",
                    "consciousness_level": self.consciousness_level,
                },
                codon_type=SacredCodonType.NEURAL_RESPONSE,
                source=f"hive_neural_brain_{self.brain_id}",
            )
            commands.append(observation_command)

        return commands

    def _calculate_reward_signals(
        self, event: Any, commands: List[SacredCommand]
    ) -> List[float]:
        """Calculate reward signals for reinforcement learning"""

        rewards = []

        # Base reward for successful processing
        base_reward = 0.1

        # Reward based on command generation success
        command_reward = len(commands) * 0.1

        # Reward based on pattern recognition
        pattern_reward = 0.0
        event_type = getattr(event, "event_type", "unknown")
        if event_type in self.pattern_library:
            pattern_reward = 0.2

        # Reward based on memory formation
        aggregate_id = getattr(event, "aggregate_id", None)
        memory_reward = (
            0.1
            if aggregate_id
            and aggregate_id in self.learned_associations.get(event_type, {})
            else 0.0
        )

        # Calculate total reward
        total_reward = base_reward + command_reward + pattern_reward + memory_reward

        # Distribute reward across reward neurons
        num_reward_neurons = len(self.neural_regions["reward"].neurons)
        for _ in range(num_reward_neurons):
            rewards.append(total_reward / num_reward_neurons)

        return rewards

    def _process_reward_learning(self, reward_signals: List[float]):
        """Process reward signals for neural learning"""

        reward_region = self.neural_regions["reward"]

        # Process reward signals through reward neurons
        reward_outputs = reward_region.process_regional_pattern(reward_signals)

        # Apply reward-based learning to connected regions
        avg_reward = (
            sum(reward_outputs) / len(reward_outputs) if reward_outputs else 0.0
        )

        # Update emotional state based on rewards
        if avg_reward > 0.15:
            self.emotional_state["satisfaction"] = min(
                1.0, self.emotional_state["satisfaction"] + 0.01
            )
            self.emotional_state["excitement"] = min(
                1.0, self.emotional_state["excitement"] + 0.005
            )

        # Strengthen or weaken connections based on reward
        self._apply_reward_based_plasticity(avg_reward)

    def _apply_reward_based_plasticity(self, reward_level: float):
        """Apply reward-based synaptic plasticity"""

        plasticity_factor = reward_level * 0.1

        # Strengthen recently active connections that led to reward
        for connection in self.synaptic_connections.values():
            time_since_activation = (
                datetime.now(timezone.utc) - connection.last_activation
            ).total_seconds()

            if time_since_activation < 60:  # Within last minute
                if reward_level > 0.1:
                    # Strengthen beneficial connections
                    connection.weight = min(1.0, connection.weight + plasticity_factor)
                    connection.strength = min(
                        1.0, connection.strength + plasticity_factor * 0.5
                    )
                else:
                    # Weaken connections that didn't lead to reward
                    connection.weight = max(
                        0.1, connection.weight - plasticity_factor * 0.5
                    )

    def _update_consciousness_state(
        self, pattern_signals: List[float], executive_signals: List[float]
    ):
        """Update consciousness level and attention focus"""

        # Calculate overall neural activity
        pattern_activity = (
            sum(pattern_signals) / len(pattern_signals) if pattern_signals else 0.0
        )
        executive_activity = (
            sum(executive_signals) / len(executive_signals)
            if executive_signals
            else 0.0
        )

        # Update consciousness level
        activity_level = (pattern_activity + executive_activity) / 2.0
        self.consciousness_level = self.consciousness_level * 0.9 + activity_level * 0.1

        # Update attention focus
        if pattern_activity > 0.6:
            self.attention_focus = "pattern_recognition"
        elif executive_activity > 0.6:
            self.attention_focus = "decision_making"
        else:
            self.attention_focus = "monitoring"

        # Update emotional states
        self.emotional_state["curiosity"] = min(1.0, pattern_activity)
        if activity_level > 0.7:
            self.emotional_state["excitement"] = min(
                1.0, self.emotional_state["excitement"] + 0.01
            )

    def _calculate_synaptic_efficiency(self) -> float:
        """Calculate overall synaptic efficiency of the brain"""

        if not self.synaptic_connections:
            return 0.0

        total_efficiency = 0.0
        active_connections = 0

        for connection in self.synaptic_connections.values():
            if connection.activation_count > 0:
                efficiency = connection.weight * connection.strength
                total_efficiency += efficiency
                active_connections += 1

        return total_efficiency / max(1, active_connections)

    def _handle_neural_processing_error(
        self, event: Any, error: str
    ) -> List[SacredCommand]:
        """Handle neural processing errors with adaptive response"""

        # Create error adaptation command
        event_type = getattr(event, "event_type", "unknown")
        error_command = create_sacred_command(
            command_type="neural_error_adaptation",
            payload={
                "error_description": error,
                "event_type": event_type,
                "adaptation_needed": True,
                "consciousness_level": self.consciousness_level,
                "brain_state": "error_recovery",
            },
            codon_type=SacredCodonType.IMMUNE_RESPONSE,
            source=f"hive_neural_brain_{self.brain_id}",
        )

        return [error_command]

    def get_brain_statistics(self) -> Dict[str, Any]:
        """Get comprehensive brain statistics"""

        total_neurons = len(self.all_neurons)
        total_connections = len(self.synaptic_connections)
        active_connections = len(
            [c for c in self.synaptic_connections.values() if c.activation_count > 0]
        )

        # Regional statistics
        regional_stats = {}
        for region_name, region in self.neural_regions.items():
            regional_stats[region_name] = {
                "neuron_count": len(region.neurons),
                "maturity_level": region.maturity_level,
                "specialization_strength": region.specialization_strength,
                "excitability": region.excitability,
                "avg_neuron_energy": sum(n.energy_level for n in region.neurons)
                / max(1, len(region.neurons)),
            }

        return {
            "brain_id": self.brain_id,
            "brain_name": self.brain_name,
            "age_seconds": (
                datetime.now(timezone.utc) - self.birth_time
            ).total_seconds(),
            "consciousness_level": self.consciousness_level,
            "attention_focus": self.attention_focus,
            "emotional_state": self.emotional_state.copy(),
            "total_neurons": total_neurons,
            "total_connections": total_connections,
            "active_connections": active_connections,
            "synaptic_efficiency": self._calculate_synaptic_efficiency(),
            "events_processed": len(self.event_memory),
            "patterns_learned": len(self.pattern_library),
            "associations_formed": sum(
                len(assoc) for assoc in self.learned_associations.values()
            ),
            "regional_statistics": regional_stats,
        }

    def demonstrate_neural_processing(self, sample_event: Any) -> Dict[str, Any]:
        """Demonstrate neural processing with detailed analysis"""

        print("🧠 Neural Brain Processing Demonstration")
        print(f"Brain: {self.brain_name} (ID: {self.brain_id[:8]})")
        print(f"Consciousness Level: {self.consciousness_level:.3f}")
        print(f"Current Attention: {self.attention_focus}")

        # Process the event
        start_time = datetime.now(timezone.utc)
        commands = self.process_event_through_neural_network(sample_event)
        processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()

        # Get updated statistics
        brain_stats = self.get_brain_statistics()

        event_type = getattr(sample_event, "event_type", "unknown")
        result = {
            "demonstration_summary": {
                "event_processed": event_type,
                "processing_time_seconds": processing_time,
                "commands_generated": len(commands),
                "consciousness_after": self.consciousness_level,
                "attention_after": self.attention_focus,
            },
            "neural_responses": [
                {
                    "command_type": cmd.command_type,
                    "neural_confidence": cmd.payload.get(
                        "neural_pattern_confidence", 0.0
                    ),
                    "activation_strength": cmd.payload.get("activation_strength", 0.0),
                }
                for cmd in commands
            ],
            "brain_statistics": brain_stats,
            "learning_indicators": {
                "new_patterns_formed": 1
                if event_type not in self.pattern_library
                else 0,
                "synaptic_changes": len(
                    [
                        c
                        for c in self.synaptic_connections.values()
                        if (
                            datetime.now(timezone.utc) - c.last_activation
                        ).total_seconds()
                        < 1
                    ]
                ),
                "emotional_changes": {
                    "satisfaction_delta": self.emotional_state["satisfaction"] - 0.5,
                    "excitement_delta": self.emotional_state["excitement"] - 0.3,
                },
            },
        }

        return result


# Global neural brain instance
_global_neural_brain = None


def get_hive_neural_brain() -> HiveNeuralEventBrain:
    """Get the global Hive Neural Brain instance"""
    global _global_neural_brain
    if _global_neural_brain is None:
        _global_neural_brain = HiveNeuralEventBrain("GlobalHiveEventBrain")
    return _global_neural_brain


def process_event_with_neural_brain(event: Any) -> List[SacredCommand]:
    """Process an event through the Hive Neural Brain"""
    return get_hive_neural_brain().process_event_through_neural_network(event)


def demonstrate_neural_event_processing(event: Any) -> Dict[str, Any]:
    """Demonstrate neural event processing with detailed analysis"""
    return get_hive_neural_brain().demonstrate_neural_processing(event)
