#!/usr/bin/env python3
"""
🧪 Chemical Architecture Blueprints
Advanced polycyclic blueprints for complex software architecture molecules.

Defines sophisticated architectural patterns based on real polycyclic aromatic hydrocarbons:
- Naphthalene: Fused dual bounded contexts (A2CX)
- Anthracene: Linear processing pipelines (A3CX)
- Phenanthrene: Branch-and-merge architectures (A3CX angular)
- Coronene: Large distributed systems (A7CX)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Any, Optional
from enum import Enum

try:
    from transformations.polycyclic_generator import (
        PolycyclicStructure,
        AdapterState,
        PolycyclicAdapter,
    )
except ImportError:
    from ..transformations.polycyclic_generator import (
        PolycyclicStructure,
        AdapterState,
        PolycyclicAdapter,
    )


class PolycyclicPattern(Enum):
    """Polycyclic architectural patterns"""

    FUSED_IDENTITY_ACCESS = "fused_identity_access"
    PAYMENT_BILLING = "payment_billing"
    ORDER_FULFILLMENT = "order_fulfillment"
    LINEAR_PIPELINE = "linear_pipeline"
    ANGULAR_BRANCH_MERGE = "angular_branch_merge"
    DISTRIBUTED_CONSTELLATION = "distributed_constellation"


@dataclass
class PolycyclicBlueprint:
    """Extended blueprint for polycyclic molecular architectures"""

    name: str
    description: str
    structure_type: str
    polycyclic_pattern: PolycyclicPattern
    chemical_structure: PolycyclicStructure
    core_domains: List[str]
    adapter_configs: List[Dict[str, Any]]
    stability_level: str = "High"
    fusion_bonds: List[Tuple[str, str]] = field(default_factory=list)
    toxic_adapters: List[str] = field(default_factory=list)
    evolution_paths: Dict[str, str] = field(default_factory=dict)
    resonance_groups: List[List[str]] = field(default_factory=list)

    def get_adapter_configs(self) -> List[PolycyclicAdapter]:
        """Convert adapter configs to PolycyclicAdapter objects"""
        adapters = []

        for config in self.adapter_configs:
            state = AdapterState.STABLE
            if config["name"] in self.toxic_adapters:
                state = AdapterState.TOXIC
            elif config["name"] in self.evolution_paths:
                state = AdapterState.EVOLVING
            elif any(config["name"] in group for group in self.resonance_groups):
                state = AdapterState.RESONANCE
            elif config.get("superposition", False):
                state = AdapterState.SUPERPOSITION

            adapter = PolycyclicAdapter(
                name=config["name"],
                state=state,
                external_connection=config.get("external"),
                bond_strength=config.get("strength", 1.0),
                evolution_target=self.evolution_paths.get(config["name"]),
                toxicity_level=config.get("toxicity", 0.0),
            )
            adapters.append(adapter)

        return adapters


class ChemicalBlueprintLibrary:
    """Library of advanced polycyclic architectural blueprints"""

    def __init__(self):
        self.blueprints = self._initialize_polycyclic_blueprints()

    def _initialize_polycyclic_blueprints(self) -> Dict[str, PolycyclicBlueprint]:
        """Initialize the polycyclic blueprint library"""
        blueprints = {}

        # A2C10 Identity+Access Pattern (Naphthalene-like)
        blueprints["fused_identity_access"] = PolycyclicBlueprint(
            name="Fused Identity+Access Core",
            description="Naphthalene-like fused dual domain for identity and access management",
            structure_type="naphthalene",
            polycyclic_pattern=PolycyclicPattern.FUSED_IDENTITY_ACCESS,
            chemical_structure=PolycyclicStructure.NAPHTHALENE,
            core_domains=["Identity", "Access"],
            adapter_configs=[
                {
                    "name": "REST",
                    "external": "Mobile",
                    "strength": 1.5,
                    "toxicity": 0.8,
                },
                {"name": "GraphQL", "external": "Web", "strength": 1.2},
                {"name": "Gateway", "external": "API_GW", "strength": 1.0},
                {"name": "DB", "external": "Postgres", "strength": 1.8},
                {"name": "EventBus", "external": "MessageQueue", "strength": 1.0},
                {"name": "Metrics", "external": "Prometheus", "strength": 0.9},
                {
                    "name": "AuthZ",
                    "external": "Policy",
                    "strength": 1.3,
                    "superposition": True,
                },
                {"name": "Cache", "external": "Redis", "strength": 1.1},
                {"name": "Audit", "external": "SIEM", "strength": 1.6},
            ],
            fusion_bonds=[("Identity", "Access")],
            toxic_adapters=["REST"],
            evolution_paths={"GraphQL": "GraphQL_v2"},
            resonance_groups=[["Gateway", "Audit"], ["AuthZ", "Policy"]],
            stability_level="Very High",
        )

        # A2C12 Payment+Billing Pattern
        blueprints["payment_billing"] = PolycyclicBlueprint(
            name="Payment+Billing Fused Core",
            description="Financial transaction processing with shared billing domain",
            structure_type="naphthalene",
            polycyclic_pattern=PolycyclicPattern.PAYMENT_BILLING,
            chemical_structure=PolycyclicStructure.NAPHTHALENE,
            core_domains=["Payment", "Billing"],
            adapter_configs=[
                {"name": "Stripe", "external": "StripeAPI", "strength": 1.9},
                {"name": "PayPal", "external": "PayPalAPI", "strength": 1.7},
                {"name": "Fraud", "external": "FraudDetect", "strength": 1.6},
                {"name": "Wallet", "external": "WalletService", "strength": 1.4},
                {"name": "Ledger", "external": "AccountingDB", "strength": 2.0},
                {"name": "Invoice", "external": "PDFGenerator", "strength": 1.1},
                {"name": "Tax", "external": "TaxService", "strength": 1.3},
                {"name": "Notification", "external": "EmailService", "strength": 1.0},
                {"name": "Reconcile", "external": "BankAPI", "strength": 1.5},
                {"name": "Analytics", "external": "DataWarehouse", "strength": 0.9},
                {"name": "Compliance", "external": "AuditLog", "strength": 1.2},
                {"name": "Webhook", "external": "EventStream", "strength": 1.1},
            ],
            fusion_bonds=[("Payment", "Billing")],
            toxic_adapters=["Webhook"],
            evolution_paths={"Stripe": "Stripe_v2", "PayPal": "PayPal_GraphQL"},
            resonance_groups=[["Fraud", "Compliance"], ["Ledger", "Reconcile"]],
            stability_level="High",
        )

        # A3C15 Order+Fulfillment+Shipping Linear Pipeline (Anthracene-like)
        blueprints["order_fulfillment_shipping"] = PolycyclicBlueprint(
            name="Order→Fulfillment→Shipping Pipeline",
            description="Linear processing chain for e-commerce order lifecycle",
            structure_type="anthracene",
            polycyclic_pattern=PolycyclicPattern.LINEAR_PIPELINE,
            chemical_structure=PolycyclicStructure.ANTHRACENE,
            core_domains=["Order", "Fulfillment", "Shipping"],
            adapter_configs=[
                {"name": "Cart", "external": "WebStore", "strength": 1.4},
                {"name": "Inventory", "external": "WMS", "strength": 1.8},
                {"name": "Payment", "external": "PaymentGW", "strength": 1.9},
                {"name": "Warehouse", "external": "WarehouseAPI", "strength": 1.7},
                {"name": "Pick", "external": "PickingSystem", "strength": 1.5},
                {"name": "Pack", "external": "PackingStation", "strength": 1.3},
                {"name": "UPS", "external": "UPSService", "strength": 1.6},
                {"name": "FedEx", "external": "FedExService", "strength": 1.6},
                {"name": "USPS", "external": "USPSService", "strength": 1.4},
                {"name": "Track", "external": "TrackingDB", "strength": 1.2},
                {"name": "Returns", "external": "RMASystem", "strength": 1.1},
                {
                    "name": "CustomerService",
                    "external": "SupportTicket",
                    "strength": 1.0,
                },
                {"name": "Analytics", "external": "OrderMetrics", "strength": 0.9},
                {"name": "Notification", "external": "SMS_Email", "strength": 1.0},
                {"name": "ERP", "external": "ERPSystem", "strength": 1.3},
            ],
            fusion_bonds=[("Order", "Fulfillment"), ("Fulfillment", "Shipping")],
            toxic_adapters=["ERP", "Returns"],
            evolution_paths={"UPS": "UPS_v2", "Inventory": "RealTimeInventory"},
            resonance_groups=[["UPS", "FedEx", "USPS"], ["Pick", "Pack"]],
            stability_level="Medium-High",
        )

        # A3C14 User+Content+Social Angular (Phenanthrene-like)
        blueprints["user_content_social"] = PolycyclicBlueprint(
            name="User⟨Content⟩Social Angular Core",
            description="Angular social platform architecture with shared content processing",
            structure_type="phenanthrene",
            polycyclic_pattern=PolycyclicPattern.ANGULAR_BRANCH_MERGE,
            chemical_structure=PolycyclicStructure.PHENANTHRENE,
            core_domains=["User", "Content", "Social"],
            adapter_configs=[
                {"name": "Auth", "external": "OAuth2", "strength": 1.7},
                {"name": "Profile", "external": "UserDB", "strength": 1.5},
                {"name": "Upload", "external": "S3Storage", "strength": 1.6},
                {"name": "CDN", "external": "CloudFront", "strength": 1.4},
                {"name": "Transcode", "external": "MediaProcessor", "strength": 1.8},
                {"name": "Search", "external": "ElasticSearch", "strength": 1.3},
                {"name": "Feed", "external": "TimelineDB", "strength": 1.9},
                {"name": "Follow", "external": "GraphDB", "strength": 1.6},
                {"name": "Like", "external": "RedisCache", "strength": 1.2},
                {"name": "Comment", "external": "CommentDB", "strength": 1.4},
                {"name": "Notification", "external": "PushService", "strength": 1.1},
                {"name": "Moderation", "external": "MLModeration", "strength": 1.5},
                {"name": "Analytics", "external": "ClickStream", "strength": 1.0},
                {"name": "Recommendation", "external": "MLEngine", "strength": 1.7},
            ],
            fusion_bonds=[
                ("User", "Content"),
                ("Content", "Social"),
                ("User", "Social"),
            ],
            toxic_adapters=["Moderation", "Analytics"],
            evolution_paths={"CDN": "EdgeCompute", "Recommendation": "TransformerML"},
            resonance_groups=[
                ["Feed", "Follow"],
                ["Like", "Comment"],
                ["Upload", "Transcode"],
            ],
            stability_level="Medium",
        )

        # A7C24 Microservices Constellation (Coronene-like)
        blueprints["microservices_constellation"] = PolycyclicBlueprint(
            name="Microservices Constellation (Super-Hexagon)",
            description="Large distributed system with 7 core domains in coronene pattern",
            structure_type="coronene",
            polycyclic_pattern=PolycyclicPattern.DISTRIBUTED_CONSTELLATION,
            chemical_structure=PolycyclicStructure.CORONENE,
            core_domains=[
                "Gateway",
                "Auth",
                "User",
                "Product",
                "Order",
                "Payment",
                "Analytics",
            ],
            adapter_configs=[
                # Gateway adapters
                {"name": "LoadBalancer", "external": "NginxLB", "strength": 1.9},
                {"name": "RateLimit", "external": "RedisRL", "strength": 1.6},
                {"name": "CORS", "external": "OriginValidator", "strength": 1.2},
                # Auth adapters
                {"name": "JWT", "external": "TokenService", "strength": 1.8},
                {"name": "OAuth", "external": "GoogleAuth", "strength": 1.7},
                {"name": "MFA", "external": "AuthenticatorApp", "strength": 1.5},
                # User adapters
                {
                    "name": "Registration",
                    "external": "EmailVerification",
                    "strength": 1.4,
                },
                {"name": "Profile", "external": "UserPreferences", "strength": 1.3},
                # Product adapters
                {"name": "Catalog", "external": "ProductDB", "strength": 1.8},
                {"name": "Search", "external": "ElasticSearch", "strength": 1.6},
                {"name": "Reviews", "external": "ReviewService", "strength": 1.2},
                # Order adapters
                {"name": "Cart", "external": "SessionStore", "strength": 1.5},
                {"name": "Checkout", "external": "CheckoutFlow", "strength": 1.9},
                # Payment adapters
                {"name": "Stripe", "external": "StripeAPI", "strength": 1.9},
                {"name": "PayPal", "external": "PayPalAPI", "strength": 1.7},
                # Analytics adapters
                {"name": "Events", "external": "EventStream", "strength": 1.3},
                {"name": "Metrics", "external": "Prometheus", "strength": 1.4},
                {"name": "Logs", "external": "LogAggregator", "strength": 1.1},
                # Shared infrastructure
                {"name": "ServiceMesh", "external": "Istio", "strength": 1.6},
                {"name": "MessageQueue", "external": "Kafka", "strength": 1.8},
                {"name": "Database", "external": "PostgresCluster", "strength": 2.0},
                {"name": "Cache", "external": "RedisCluster", "strength": 1.7},
                {"name": "Storage", "external": "S3Bucket", "strength": 1.5},
                {"name": "CDN", "external": "CloudFront", "strength": 1.4},
                {"name": "Monitoring", "external": "Grafana", "strength": 1.2},
            ],
            fusion_bonds=[
                ("Gateway", "Auth"),
                ("Auth", "User"),
                ("User", "Product"),
                ("Product", "Order"),
                ("Order", "Payment"),
                ("Payment", "Analytics"),
                ("Analytics", "Gateway"),  # Completes the ring
            ],
            toxic_adapters=["CORS", "Logs", "Reviews"],
            evolution_paths={
                "JWT": "PasskeyAuth",
                "Stripe": "CryptoPayments",
                "ElasticSearch": "VectorSearch",
            },
            resonance_groups=[
                ["LoadBalancer", "ServiceMesh"],
                ["Cache", "Database"],
                ["Stripe", "PayPal"],
                ["Events", "Metrics"],
            ],
            stability_level="Complex-High",
        )

        return blueprints

    def get_blueprint(self, pattern: str) -> Optional[PolycyclicBlueprint]:
        """Get a specific polycyclic blueprint"""
        return self.blueprints.get(pattern)

    def list_blueprints(self) -> List[str]:
        """List all available blueprint names"""
        return list(self.blueprints.keys())

    def get_blueprint_catalog(self) -> Dict[str, Dict[str, Any]]:
        """Get full catalog of blueprints with metadata"""
        catalog = {}

        for name, blueprint in self.blueprints.items():
            catalog[name] = {
                "name": blueprint.name,
                "description": blueprint.description,
                "pattern": blueprint.polycyclic_pattern.value,
                "structure": blueprint.chemical_structure.value,
                "core_count": len(blueprint.core_domains),
                "adapter_count": len(blueprint.adapter_configs),
                "stability": blueprint.stability_level,
                "has_toxic_adapters": len(blueprint.toxic_adapters) > 0,
                "evolution_paths": len(blueprint.evolution_paths),
                "fusion_bonds": blueprint.fusion_bonds,
                "complexity": self._calculate_complexity(blueprint),
            }

        return catalog

    def _calculate_complexity(self, blueprint: PolycyclicBlueprint) -> str:
        """Calculate architectural complexity level"""
        score = (
            len(blueprint.core_domains) * 2
            + len(blueprint.adapter_configs) * 1
            + len(blueprint.toxic_adapters) * 3
            + len(blueprint.evolution_paths) * 2
            + sum(len(group) for group in blueprint.resonance_groups)
        )

        if score < 20:
            return "Simple"
        elif score < 40:
            return "Medium"
        elif score < 70:
            return "Complex"
        else:
            return "Enterprise"


if __name__ == "__main__":
    # Test the blueprint library
    library = ChemicalBlueprintLibrary()

    print("🧪 Polycyclic Architecture Blueprint Library")
    print("=" * 50)

    catalog = library.get_blueprint_catalog()
    for name, info in catalog.items():
        print(f"\n🧬 {info['name']}")
        print(f"   Pattern: {info['pattern']} ({info['structure']})")
        print(f"   Cores: {info['core_count']} | Adapters: {info['adapter_count']}")
        print(f"   Complexity: {info['complexity']} | Stability: {info['stability']}")
        print(
            f"   Toxic: {info['has_toxic_adapters']} | Evolution: {info['evolution_paths']}"
        )
