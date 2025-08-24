"""
Hive Neural Event Brain Demonstration - Bio/Sci Intelligence

This demo showcases the brain-like neural network event processing system
that follows bio/sci nature/orgs philosophy. Neural networks learn, adapt,
and form synaptic connections while processing events through specialized
brain regions like a biological brain.

Key Demonstrations:
- Neural network event processing through brain regions
- Synaptic learning and connection strengthening
- Memory formation and pattern recognition
- Consciousness and attention dynamics
- Reward-based reinforcement learning
- Brain region specialization and maturation
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Dict, Any

# Create a simple mock PollenEnvelope for demonstration
@dataclass
class MockPollenEnvelope:
    event_id: str
    event_type: str
    event_version: str
    aggregate_id: str
    timestamp: datetime
    payload: Dict[str, Any]

from dna_core.royal_jelly.neural_event_brain import (
    HiveNeuralEventBrain,
    get_hive_neural_brain,
    NeuronType,
    ActivationFunction
)


def create_sample_event(event_type: str, aggregate_id: str = "neural_test_aggregate") -> MockPollenEnvelope:
    """Create a sample event for neural processing"""
    
    return MockPollenEnvelope(
        event_id=f"neural_test_{event_type.lower().replace(' ', '_')}",
        event_type=event_type,
        event_version="2.0",
        aggregate_id=aggregate_id,
        timestamp=datetime.now(timezone.utc),
        payload={
            "message": f"Neural brain processing test for {event_type}",
            "complexity": len(event_type),
            "neural_test": True,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )


def demonstrate_neural_brain_architecture():
    """Demonstrate the neural brain architecture and brain regions"""
    
    print("🧠 === HIVE NEURAL EVENT BRAIN ARCHITECTURE DEMO ===")
    print()
    
    # Get the global neural brain
    neural_brain = get_hive_neural_brain()
    
    print(f"🧬 Brain Identity:")
    print(f"   Name: {neural_brain.brain_name}")
    print(f"   ID: {neural_brain.brain_id[:12]}...")
    print(f"   Birth Time: {neural_brain.birth_time}")
    print()
    
    # Show brain regions
    print(f"🏛️ Brain Region Architecture:")
    for region_name, region in neural_brain.neural_regions.items():
        print(f"   📍 {region.region_name} ({region_name}):")
        print(f"      Function: {region.specialized_function}")
        print(f"      Neurons: {len(region.neurons)}")
        print(f"      Maturity: {region.maturity_level:.3f}")
        print(f"      Excitability: {region.excitability:.3f}")
        print()
    
    # Show neural connections
    total_connections = len(neural_brain.synaptic_connections)
    active_connections = len([c for c in neural_brain.synaptic_connections.values() if c.activation_count > 0])
    
    print(f"🕸️ Neural Connectivity:")
    print(f"   Total Synapses: {total_connections}")
    print(f"   Active Synapses: {active_connections}")
    print(f"   Connectivity Rate: {(total_connections / max(1, len(neural_brain.all_neurons)) * 100):.1f}%")
    print()
    
    return neural_brain


def demonstrate_event_processing_pipeline():
    """Demonstrate the complete neural event processing pipeline"""
    
    print("⚡ === NEURAL EVENT PROCESSING PIPELINE ===")
    print()
    
    neural_brain = get_hive_neural_brain()
    
    # Create different types of events to show neural adaptation
    test_events = [
        create_sample_event("UserRegistration"),
        create_sample_event("PaymentProcessing"),
        create_sample_event("DataAnalysis"),
        create_sample_event("SystemMaintenance"),
        create_sample_event("SecurityAlert")
    ]
    
    print("🔄 Processing Events Through Neural Pipeline:")
    print()
    
    for i, event in enumerate(test_events):
        print(f"📨 Event {i+1}: {event.event_type}")
        print(f"   Aggregate: {event.aggregate_id}")
        print(f"   Version: {event.event_version}")
        
        # Process through neural brain
        start_consciousness = neural_brain.consciousness_level
        start_attention = neural_brain.attention_focus
        
        commands = neural_brain.process_event_through_neural_network(event)
        
        print(f"   🧠 Consciousness: {start_consciousness:.3f} → {neural_brain.consciousness_level:.3f}")
        print(f"   👁️ Attention: {start_attention} → {neural_brain.attention_focus}")
        print(f"   ⚡ Neural Responses: {len(commands)}")
        
        for j, command in enumerate(commands[:2]):  # Show first 2 commands
            confidence = command.payload.get("neural_pattern_confidence", 0.0)
            activation = command.payload.get("activation_strength", 0.0)
            print(f"      {j+1}. {command.command_type}")
            print(f"         Confidence: {confidence:.3f}")
            print(f"         Activation: {activation:.3f}")
        
        print()
    
    return commands


def demonstrate_neural_learning_and_memory():
    """Demonstrate neural learning, memory formation, and pattern recognition"""
    
    print("🎓 === NEURAL LEARNING AND MEMORY FORMATION ===")
    print()
    
    neural_brain = get_hive_neural_brain()
    
    # Before learning state
    initial_patterns = len(neural_brain.pattern_library)
    initial_associations = sum(len(assoc) for assoc in neural_brain.learned_associations.values())
    
    print(f"📚 Initial Learning State:")
    print(f"   Patterns Learned: {initial_patterns}")
    print(f"   Associations Formed: {initial_associations}")
    print(f"   Events Processed: {len(neural_brain.event_memory)}")
    print()
    
    # Process repeated events to show learning
    print("🔄 Processing Repeated Events for Learning:")
    
    learning_event = create_sample_event("RepeatedLearningPattern")
    
    for round in range(3):
        print(f"   Learning Round {round + 1}:")
        
        # Process the same type of event multiple times
        for i in range(5):
            commands = neural_brain.process_event_through_neural_network(learning_event)
            
        # Check learning progress
        current_patterns = len(neural_brain.pattern_library)
        current_associations = sum(len(assoc) for assoc in neural_brain.learned_associations.values())
        synaptic_efficiency = neural_brain._calculate_synaptic_efficiency()
        
        print(f"      Patterns: {current_patterns}")
        print(f"      Associations: {current_associations}")
        print(f"      Synaptic Efficiency: {synaptic_efficiency:.3f}")
        
        # Show strongest connections
        strong_connections = [c for c in neural_brain.synaptic_connections.values() if c.weight > 0.7]
        print(f"      Strong Connections: {len(strong_connections)}")
        print()
    
    # Show memory contents
    print("🧠 Memory Formation Results:")
    if neural_brain.pattern_library:
        for pattern_key in list(neural_brain.pattern_library.keys())[:3]:
            pattern_strength = sum(neural_brain.pattern_library[pattern_key]) / len(neural_brain.pattern_library[pattern_key])
            print(f"   Pattern '{pattern_key}': strength {pattern_strength:.3f}")
    
    if neural_brain.learned_associations:
        for event_type, associations in list(neural_brain.learned_associations.items())[:2]:
            print(f"   Event '{event_type}': {len(associations)} associations")
    
    print()


def demonstrate_brain_consciousness_and_emotions():
    """Demonstrate consciousness dynamics and emotional states"""
    
    print("🧘 === CONSCIOUSNESS AND EMOTIONAL DYNAMICS ===")
    print()
    
    neural_brain = get_hive_neural_brain()
    
    print(f"🌟 Current Consciousness State:")
    print(f"   Consciousness Level: {neural_brain.consciousness_level:.3f}")
    print(f"   Attention Focus: {neural_brain.attention_focus}")
    print()
    
    print(f"😊 Emotional Profile:")
    for emotion, level in neural_brain.emotional_state.items():
        emotion_bar = "█" * int(level * 20) + "░" * (20 - int(level * 20))
        print(f"   {emotion.capitalize():12} [{emotion_bar}] {level:.3f}")
    print()
    
    # Process different events to show emotional responses
    print("🎭 Emotional Response to Different Events:")
    
    emotional_test_events = [
        ("SystemSuccess", "positive"),
        ("ErrorOccurred", "stressful"),
        ("NewDiscovery", "exciting"),
        ("RoutineTask", "neutral")
    ]
    
    for event_name, expected_emotion in emotional_test_events:
        # Store pre-event emotional state
        pre_emotions = neural_brain.emotional_state.copy()
        pre_consciousness = neural_brain.consciousness_level
        
        # Process event
        test_event = create_sample_event(event_name)
        commands = neural_brain.process_event_through_neural_network(test_event)
        
        # Show emotional changes
        print(f"   📨 {event_name} ({expected_emotion}):")
        print(f"      Consciousness: {pre_consciousness:.3f} → {neural_brain.consciousness_level:.3f}")
        
        for emotion in ["curiosity", "satisfaction", "stress", "excitement"]:
            change = neural_brain.emotional_state[emotion] - pre_emotions[emotion]
            if abs(change) > 0.001:
                direction = "↑" if change > 0 else "↓"
                print(f"      {emotion.capitalize()}: {direction} {abs(change):.3f}")
        print()


def demonstrate_brain_region_specialization():
    """Demonstrate how brain regions specialize and mature"""
    
    print("🏗️ === BRAIN REGION SPECIALIZATION AND MATURATION ===")
    print()
    
    neural_brain = get_hive_neural_brain()
    
    # Show regional development
    print("🧠 Regional Development Status:")
    
    for region_name, region in neural_brain.neural_regions.items():
        print(f"   📍 {region.region_name}:")
        print(f"      Specialization: {region.specialized_function}")
        print(f"      Maturity Level: {region.maturity_level:.3f}")
        print(f"      Specialization Strength: {region.specialization_strength:.3f}")
        print(f"      Plasticity: {region.plasticity:.3f}")
        
        # Calculate average neuron energy in region
        if region.neurons:
            avg_energy = sum(n.energy_level for n in region.neurons) / len(region.neurons)
            avg_stress = sum(n.stress_level for n in region.neurons) / len(region.neurons)
            print(f"      Average Neuron Energy: {avg_energy:.3f}")
            print(f"      Average Neuron Stress: {avg_stress:.3f}")
        
        print()
    
    # Show neuron type distribution
    neuron_type_counts = {}
    for neuron in neural_brain.all_neurons.values():
        neuron_type = neuron.neuron_type.value
        neuron_type_counts[neuron_type] = neuron_type_counts.get(neuron_type, 0) + 1
    
    print("🔬 Neuron Type Distribution:")
    for neuron_type, count in neuron_type_counts.items():
        print(f"   {neuron_type.replace('_', ' ').title()}: {count} neurons")
    print()


def demonstrate_comprehensive_brain_analysis():
    """Demonstrate comprehensive brain analysis and statistics"""
    
    print("📊 === COMPREHENSIVE BRAIN ANALYSIS ===")
    print()
    
    neural_brain = get_hive_neural_brain()
    
    # Get detailed brain statistics
    brain_stats = neural_brain.get_brain_statistics()
    
    print("🧬 Brain Vital Statistics:")
    print(f"   Age: {brain_stats['age_seconds']:.1f} seconds")
    print(f"   Total Neurons: {brain_stats['total_neurons']}")
    print(f"   Total Connections: {brain_stats['total_connections']}")
    print(f"   Active Connections: {brain_stats['active_connections']}")
    print(f"   Synaptic Efficiency: {brain_stats['synaptic_efficiency']:.3f}")
    print(f"   Events Processed: {brain_stats['events_processed']}")
    print(f"   Patterns Learned: {brain_stats['patterns_learned']}")
    print(f"   Associations Formed: {brain_stats['associations_formed']}")
    print()
    
    print("🧠 Current Brain State:")
    print(f"   Consciousness: {brain_stats['consciousness_level']:.3f}")
    print(f"   Attention: {brain_stats['attention_focus']}")
    print("   Emotional State:")
    for emotion, level in brain_stats['emotional_state'].items():
        print(f"      {emotion.capitalize()}: {level:.3f}")
    print()
    
    # Regional analysis
    print("🏛️ Regional Analysis:")
    for region_name, regional_data in brain_stats['regional_statistics'].items():
        print(f"   {region_name.title()} Region:")
        for metric, value in regional_data.items():
            if isinstance(value, float):
                print(f"      {metric.replace('_', ' ').title()}: {value:.3f}")
            else:
                print(f"      {metric.replace('_', ' ').title()}: {value}")
        print()


def run_complete_neural_brain_demonstration():
    """Run the complete neural brain demonstration"""
    
    print("🧠 ===== HIVE NEURAL EVENT BRAIN COMPLETE DEMONSTRATION =====")
    print("🌟 Bio/Sci Intelligence: Software that thinks, learns, and adapts")
    print("=" * 70)
    print()
    
    try:
        # 1. Architecture demonstration
        neural_brain = demonstrate_neural_brain_architecture()
        
        # 2. Event processing pipeline
        commands = demonstrate_event_processing_pipeline()
        
        # 3. Learning and memory
        demonstrate_neural_learning_and_memory()
        
        # 4. Consciousness and emotions
        demonstrate_brain_consciousness_and_emotions()
        
        # 5. Brain region specialization
        demonstrate_brain_region_specialization()
        
        # 6. Comprehensive analysis
        demonstrate_comprehensive_brain_analysis()
        
        print("✅ === NEURAL BRAIN DEMONSTRATION COMPLETE ===")
        print()
        print("🧬 Bio/Sci Achievement: Successfully demonstrated:")
        print("   ✓ Brain-like neural network architecture")
        print("   ✓ Synaptic learning and memory formation") 
        print("   ✓ Consciousness and emotional dynamics")
        print("   ✓ Regional specialization and maturation")
        print("   ✓ Event processing through neural pathways")
        print("   ✓ Adaptive intelligence and pattern recognition")
        print()
        print("🌟 The Hive now processes events through living neural intelligence!")
        
        return True
        
    except Exception as e:
        print(f"❌ Neural brain demonstration error: {e}")
        return False


if __name__ == "__main__":
    success = run_complete_neural_brain_demonstration()
    if success:
        print("\n🧠 Neural Event Brain system is ready for bio/sci intelligence!")
    else:
        print("\n⚠️ Neural Event Brain demonstration encountered issues.")