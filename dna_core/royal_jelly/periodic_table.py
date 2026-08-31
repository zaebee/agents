from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
from rich.table import Table
from rich.console import Console

class ElementSymbol(Enum):
    A = "🟨"  # Aggregate (Alkali Metal - Yellow)
    T = "🟩"  # Transform (Alkaline Earth - Green)
    C = "🔵"  # Connector (Transition Metal - Blue)
    G = "🟦"  # Genesis Event (Boron Group - Dark Blue)
    O = "⚫"  # Orchestrator (Carbon Group - Black)
    R = "🟪"  # Router (Nitrogen Group - Purple)
    M = "🟥"  # Monitor (Chalcogen - Red)
    H = "🟧"  # Hybrid (Halogen - Orange)

@dataclass
class PrimitiveElement:
    name: str
    symbol: ElementSymbol
    valency: tuple  # (inputs, outputs)
    reactivity: int  # 1-5 scale
    state: str  # "stateful" or "stateless"
    toxicity: str  # "low", "medium", "high"
    description: str

class PeriodicTable:
    ELEMENTS: Dict[str, PrimitiveElement] = {
        "OrderAggregate": PrimitiveElement(
            name="OrderAggregate",
            symbol=ElementSymbol.A,
            valency=(1, 1),
            reactivity=4,
            state="stateful",
            toxicity="low",
            description="Encapsulates order state and business rules."
        ),
        "PricingTransform": PrimitiveElement(
            name="PricingTransform",
            symbol=ElementSymbol.T,
            valency=(1, 1),
            reactivity=2,
            state="stateless",
            toxicity="low",
            description="Calculates pricing based on order data."
        ),
        "RestConnector": PrimitiveElement(
            name="RestConnector",
            symbol=ElementSymbol.C,
            valency=(1, 1),
            reactivity=5,
            state="stateless",
            toxicity="medium",
            description="Adapts HTTP requests to domain commands."
        ),
        "OrderPlacedEvent": PrimitiveElement(
            name="OrderPlacedEvent",
            symbol=ElementSymbol.G,
            valency=(0, 0),  # Events are inert until consumed
            reactivity=1,
            state="stateless",
            toxicity="low",
            description="Immutable fact: an order was placed."
        ),
        "SagaOrchestrator": PrimitiveElement(
            name="SagaOrchestrator",
            symbol=ElementSymbol.O,
            valency=(1, 3),  # 1 input, 3+ output commands
            reactivity=5,
            state="stateful",
            toxicity="high",
            description="Manages long-running sagas (e.g., order fulfillment)."
        ),
        "EventRouter": PrimitiveElement(
            name="EventRouter",
            symbol=ElementSymbol.R,
            valency=(1, 1),
            reactivity=4,
            state="stateful",
            toxicity="medium",
            description="Routes events to appropriate consumers."
        ),
        "MetricMonitor": PrimitiveElement(
            name="MetricMonitor",
            symbol=ElementSymbol.M,
            valency=(1, 1),
            reactivity=3,
            state="stateless",
            toxicity="low",
            description="Observes events and emits metrics."
        ),
        "RestApiAggregate": PrimitiveElement(
            name="RestApiAggregate",
            symbol=ElementSymbol.H,
            valency=(1, 1),
            reactivity=5,
            state="stateful",
            toxicity="high",
            description="Hybrid: Connector + Aggregate (anti-pattern!)."
        )
    }

    @classmethod
    def print_table(cls):
        console = Console()
        table = Table(title="🧪 The Hive's Periodic Table of Software Primitives")

        # Columns
        table.add_column("Group", style="cyan")
        table.add_column("1 (A)", style="yellow")
        table.add_column("2 (T)", style="green")
        table.add_column("3-12 (C)", style="blue")
        table.add_column("13 (G)", style="dark_blue")
        table.add_column("14 (O)", style="white on black")
        table.add_column("15 (R)", style="purple")
        table.add_column("16 (M)", style="red")
        table.add_column("17-18 (H)", style="orange1")

        # Rows (Periods)
        table.add_row(
            "[bold]1[/bold]",
            "OrderAggregate\n🟨 A (1,1)",
            "PricingTransform\n🟩 T (1,1)",
            "RestConnector\n🔵 C (1,1)",
            "OrderPlacedEvent\n🟦 G (0,0)",
            "-",
            "-",
            "-",
            "-"
        )
        table.add_row(
            "[bold]2[/bold]",
            "UserAggregate\n🟨 A (1,1)",
            "ReportTransform\n🟩 T (1,1)",
            "DbConnector\n🔵 C (1,1)",
            "PaymentEvent\n🟦 G (0,0)",
            "SagaOrchestrator\n⚫ O (1,3)",
            "EventRouter\n🟪 R (1,1)",
            "MetricMonitor\n🟥 M (1,1)",
            "RestApiAggregate\n🟧 H (1,1)"
        )

        console.print(table)

    @classmethod
    def get_element(cls, name: str) -> Optional[PrimitiveElement]:
        # A simple search, can be optimized
        for k, v in cls.ELEMENTS.items():
            if k.lower() == name.lower():
                return v
        return None

    @classmethod
    def predict_compatibility(cls, element_name1: str, element_name2: str) -> bool:
        """Predict if two primitives can bond (like chemical reactivity)."""
        e1 = cls.get_element(element_name1)
        e2 = cls.get_element(element_name2)
        if not e1 or not e2:
            return False

        # Example rule: Aggregates (A) bond with Events (G) as input for other things
        # This is a placeholder for more complex bonding logic
        if e1.symbol == ElementSymbol.A and e2.symbol == ElementSymbol.G:
            return True
        if e1.symbol == ElementSymbol.M and e2.symbol == ElementSymbol.G:
            return True

        return False

    @classmethod
    def check_toxicity(cls, element_name: str) -> str:
        """Check if a primitive is toxic (high-risk)."""
        e = cls.get_element(element_name)
        return e.toxicity if e else "unknown"
