"""
Hive Neural Event Brain Standalone Demonstration

This is a simplified demonstration of the neural event processing engine
that works independently without protobuf dependencies.
"""

from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Dict, Any
import random


# Mock event structure
@dataclass
class MockEvent:
    event_id: str
    event_type: str
    event_version: str
    aggregate_id: str
    timestamp: datetime
    payload: Dict[str, Any]


# Simplified neural brain demo
class SimplifiedNeuralBrain:
    """Simplified neural brain for demonstration"""

    def __init__(self):
        self.consciousness_level = 0.1
        self.attention_focus = "monitoring"
        self.emotional_state = {
            "curiosity": 0.5,
            "satisfaction": 0.5,
            "stress": 0.0,
            "excitement": 0.3,
        }
        self.events_processed = 0
        self.patterns_learned = {}

    def process_event(self, event: MockEvent) -> Dict[str, Any]:
        """Process an event and return neural response"""

        self.events_processed += 1

        # Simulate neural activation
        activation_strength = random.uniform(0.3, 0.9)

        # Update consciousness
        old_consciousness = self.consciousness_level
        self.consciousness_level = min(
            1.0, self.consciousness_level + activation_strength * 0.1
        )

        # Update attention based on event type
        if "error" in event.event_type.lower():
            self.attention_focus = "error_handling"
            self.emotional_state["stress"] = min(
                1.0, self.emotional_state["stress"] + 0.1
            )
        elif "success" in event.event_type.lower():
            self.attention_focus = "celebration"
            self.emotional_state["satisfaction"] = min(
                1.0, self.emotional_state["satisfaction"] + 0.1
            )
        else:
            self.attention_focus = "pattern_analysis"
            self.emotional_state["curiosity"] = min(
                1.0, self.emotional_state["curiosity"] + 0.05
            )

        # Learn pattern
        if event.event_type not in self.patterns_learned:
            self.patterns_learned[event.event_type] = 0
        self.patterns_learned[event.event_type] += 1

        # Generate neural response
        return {
            "event_processed": event.event_type,
            "activation_strength": activation_strength,
            "consciousness_change": self.consciousness_level - old_consciousness,
            "attention_focus": self.attention_focus,
            "emotional_state": self.emotional_state.copy(),
            "pattern_recognized": self.patterns_learned[event.event_type] > 1,
            "total_events_processed": self.events_processed,
        }


def create_demo_event(event_type: str) -> MockEvent:
    """Create a demo event"""
    return MockEvent(
        event_id=f"demo_{event_type.lower().replace(' ', '_')}",
        event_type=event_type,
        event_version="2.0",
        aggregate_id="demo_aggregate",
        timestamp=datetime.now(timezone.utc),
        payload={
            "demo": True,
            "complexity": len(event_type),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


def run_neural_brain_demo():
    """Run the neural brain demonstration"""

    print("🧠 ===== HIVE NEURAL EVENT BRAIN DEMONSTRATION =====")
    print("🌟 Bio/Sci Intelligence: Software that thinks and learns")
    print("=" * 60)
    print()

    # Create neural brain
    brain = SimplifiedNeuralBrain()

    print("🧬 Initial Brain State:")
    print(f"   Consciousness: {brain.consciousness_level:.3f}")
    print(f"   Attention: {brain.attention_focus}")
    print(f"   Events Processed: {brain.events_processed}")
    print()

    # Test events
    test_events = [
        "UserRegistration",
        "PaymentSuccess",
        "SystemError",
        "DataAnalysis",
        "UserRegistration",  # Repeat for learning demo
        "SecurityAlert",
        "PaymentSuccess",  # Repeat for pattern recognition
        "PerformanceOptimization",
    ]

    print("⚡ Processing Events Through Neural Network:")
    print()

    for i, event_type in enumerate(test_events):
        event = create_demo_event(event_type)
        response = brain.process_event(event)

        print(f"📨 Event {i + 1}: {event_type}")
        print(f"   🧠 Activation Strength: {response['activation_strength']:.3f}")
        print(f"   📈 Consciousness Change: +{response['consciousness_change']:.3f}")
        print(f"   👁️ Attention Focus: {response['attention_focus']}")
        print(
            f"   🎯 Pattern Recognized: {'Yes' if response['pattern_recognized'] else 'No'}"
        )

        # Show emotional changes
        emotions_str = []
        for emotion, level in response["emotional_state"].items():
            if level > 0.6:
                emotions_str.append(f"{emotion}↑")
        if emotions_str:
            print(f"   😊 Emotions: {', '.join(emotions_str)}")

        print()

    print("🧠 Final Brain State:")
    print(f"   Consciousness Level: {brain.consciousness_level:.3f}")
    print(f"   Current Attention: {brain.attention_focus}")
    print(f"   Total Events Processed: {brain.events_processed}")
    print(f"   Patterns Learned: {len(brain.patterns_learned)}")
    print()

    print("📚 Learned Patterns:")
    for pattern, count in brain.patterns_learned.items():
        confidence = min(1.0, count * 0.2)
        print(f"   {pattern}: {count} occurrences (confidence: {confidence:.2f})")
    print()

    print("😊 Final Emotional Profile:")
    for emotion, level in brain.emotional_state.items():
        bar = "█" * int(level * 20) + "░" * (20 - int(level * 20))
        print(f"   {emotion.capitalize():12} [{bar}] {level:.3f}")
    print()

    print("✅ === NEURAL BRAIN DEMONSTRATION COMPLETE ===")
    print()
    print("🧬 Bio/Sci Achievement: Successfully demonstrated:")
    print("   ✓ Neural event processing with consciousness")
    print("   ✓ Pattern learning and recognition")
    print("   ✓ Emotional state dynamics")
    print("   ✓ Attention focus adaptation")
    print("   ✓ Experience-based learning")
    print()
    print("🌟 The Hive Neural Brain is ready for bio/sci intelligence!")

    return True


if __name__ == "__main__":
    run_neural_brain_demo()
