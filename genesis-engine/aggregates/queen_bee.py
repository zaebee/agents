#!/usr/bin/env python3
"""
The Queen Bee Aggregate - Orchestrator of the Molecular Hive
The ultimate coordinator that brings together all molecular chemistry components.

This aggregate implements the complete "Chemical Architecture" system,
coordinating honeyprint generation, stability analysis, reaction processing,
and component registry management.
"""

import json
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timezone
import asyncio

# Import our molecular chemistry components
from ..transformations.honeyprint_generator import (
    HoneyprintGenerator, 
    HoneyprintMolecule, 
    MolecularAtom, 
    MolecularElement
)
from ..transformations.reaction_engine import (
    ReactionEngine, 
    ChemicalReaction, 
    ReactionType,
    ReactionResult
)
from .molecular_analyzer import (
    MolecularAnalyzer, 
    MolecularStabilityReport,
    ArchitecturalStability
)
from ..connectors.chemical_registry import (
    ChemicalRegistry, 
    MolecularComponent,
    ComponentStability,
    SearchQuery
)

@dataclass
class BeekeeperWisdom:
    """Represents the Beekeeper's Intent - Level 7 of the Hive"""
    mission: str  # The 'why' behind the architecture
    principles: List[str]  # Guiding principles
    values: Dict[str, float]  # Weighted values (0.0 to 1.0)
    philosophy: str  # Architectural philosophy
    sacred_constraints: List[str]  # Non-negotiable rules

@dataclass
class ArchitecturalBlueprint:
    """A complete architectural blueprint with molecular specifications"""
    name: str
    description: str
    target_stability: ArchitecturalStability
    required_elements: Dict[str, int]
    suggested_reactions: List[str]
    honeyprint_config: Dict[str, Any]
    beekeeper_intent: Optional[BeekeeperWisdom] = None  # Level 7 guidance
    constraints: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BuildResult:
    """Result of building an architectural component"""
    success: bool
    component_id: Optional[str]
    honeyprint_svg: Optional[str] 
    stability_report: Optional[MolecularStabilityReport]
    reaction_results: List[ReactionResult]
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

class QueenBee:
    """
    The Queen Bee - Master orchestrator of the molecular Hive architecture.
    
    Responsibilities:
    - Coordinate all molecular chemistry subsystems
    - Process architectural blueprints
    - Generate components with full molecular analysis
    - Maintain system-wide architectural integrity
    - Provide intelligent recommendations and optimizations
    """
    
    def __init__(self, hive_root: str = "hive/components"):
        self.hive_root = Path(hive_root)
        self.hive_root.mkdir(parents=True, exist_ok=True)
        
        # Initialize all subsystems
        self.honeyprint_generator = HoneyprintGenerator()
        self.reaction_engine = ReactionEngine()
        self.molecular_analyzer = MolecularAnalyzer()
        self.chemical_registry = ChemicalRegistry()
        
        # Level 7: Beekeeper's Intent - The philosophical foundation
        self.beekeeper_wisdom = BeekeeperWisdom(
            mission="Build living, adaptive software ecosystems that serve humanity with grace and resilience",
            principles=[
                "Every component must have a clear purpose",
                "Simplicity is the ultimate sophistication",
                "Architecture should be self-healing and adaptive",
                "Code should be a gift to future maintainers",
                "Sacred patterns must be preserved",
                "Growth should be organic, not chaotic"
            ],
            values={
                "maintainability": 0.9,
                "resilience": 0.8,
                "simplicity": 0.85,
                "beauty": 0.7,
                "performance": 0.75,
                "security": 0.9,
                "collaboration": 0.8
            },
            philosophy="We build not just for today's problems, but for tomorrow's possibilities. Every line of code is a seed that may grow into something greater.",
            sacred_constraints=[
                "Never compromise the ATCG genetic code integrity",
                "Sacred Codons must be validated before synthesis",
                "Immune System responses are non-negotiable",
                "The Queen's wisdom must guide all architectural decisions",
                "Beauty and function must coexist in harmony"
            ]
        )
        
        # Component tracking
        self._active_components: Dict[str, MolecularComponent] = {}
        self._blueprint_library: Dict[str, ArchitecturalBlueprint] = {}
        
        # Performance metrics enhanced with Intent metrics
        self._build_history: List[Tuple[datetime, BuildResult]] = []
        self._system_health: Dict[str, float] = {
            "stability_score": 85.0,
            "complexity_index": 42.0,
            "coupling_coefficient": 0.15,
            "aromatic_ratio": 0.25,
            "wisdom_alignment": 0.9,  # How well we follow Beekeeper's Intent
            "purpose_clarity": 0.8,   # How clear component purposes are
            "beauty_index": 0.75      # Aesthetic and elegant design score
        }
        
        self._initialize_blueprint_library()
        
        print("👑 Queen Bee initialized with Beekeeper's Wisdom - Molecular Hive Architecture System ready!")
        print(f"📜 Mission: {self.beekeeper_wisdom.mission}")
        print(f"🎯 Core Values: {', '.join(k for k, v in self.beekeeper_wisdom.values.items() if v >= 0.8)}")
    
    def _initialize_blueprint_library(self):
        """Initialize the standard architectural blueprint library"""
        
        # Hexagonal Architecture Blueprint
        self._blueprint_library["hexagonal_core"] = ArchitecturalBlueprint(
            name="Hexagonal Architecture Core",
            description="Stable hexagonal core with 6 adapter connections (benzene-inspired)",
            target_stability=ArchitecturalStability.AROMATIC,
            required_elements={'A': 1, 'C': 6},
            suggested_reactions=["hexagonal_formation"],
            honeyprint_config={
                "core_name": "Domain Core",
                "adapters": ["REST", "gRPC", "SQL", "Events", "Auth", "CLI"],
                "external_connections": {
                    "REST": "User Interface",
                    "SQL": "Database",
                    "Events": "Message Bus"
                }
            },
            beekeeper_intent=BeekeeperWisdom(
                mission="Create adaptable cores that protect business logic while enabling flexible integration",
                principles=[
                    "Business logic must remain pure and testable",
                    "External adapters should be easily replaceable",
                    "The core should never depend on infrastructure"
                ],
                values={
                    "maintainability": 0.95,
                    "resilience": 0.9,
                    "simplicity": 0.8,
                    "beauty": 0.85
                },
                philosophy="Like a benzene ring, the hexagonal architecture achieves stability through balanced connections and aromatic resonance",
                sacred_constraints=[
                    "Core domain must never import infrastructure",
                    "All external dependencies must go through adapters",
                    "Hexagonal symmetry must be preserved"
                ]
            ),
            constraints={
                "max_adapters": 8,
                "min_bond_energy": 300.0,
                "required_patterns": ["repository", "service"]
            }
        )
        
        # Microservice Blueprint
        self._blueprint_library["microservice"] = ArchitecturalBlueprint(
            name="Microservice Component",
            description="Lightweight service with command/query handlers",
            target_stability=ArchitecturalStability.STABLE,
            required_elements={'A': 1, 'T': 2, 'C': 2, 'G': 1},
            suggested_reactions=["command_handler_synthesis", "query_handler_synthesis"],
            honeyprint_config={
                "core_name": "Service Core",
                "adapters": ["HTTP", "Database"],
                "external_connections": {"HTTP": "API Gateway"}
            },
            constraints={
                "max_complexity": 50,
                "single_responsibility": True
            }
        )
        
        # Event-Driven Architecture Blueprint
        self._blueprint_library["event_driven"] = ArchitecturalBlueprint(
            name="Event-Driven Architecture",
            description="Event-centric architecture with choreography",
            target_stability=ArchitecturalStability.STABLE,
            required_elements={'G': 3, 'C': 4, 'A': 2},
            suggested_reactions=["event_generation", "choreography_synthesis"],
            honeyprint_config={
                "core_name": "Event Hub",
                "adapters": ["EventBus", "Saga", "Projection", "Handler"],
                "external_connections": {
                    "EventBus": "Message Stream",
                    "Saga": "Orchestrator"
                }
            },
            constraints={
                "eventual_consistency": True,
                "message_ordering": "partial"
            }
        )
        
        # Immune System Blueprint
        self._blueprint_library["immune_system"] = ArchitecturalBlueprint(
            name="Immune System Component", 
            description="Self-healing architecture with mutation detection",
            target_stability=ArchitecturalStability.AROMATIC,
            required_elements={'G': 2, 'C': 2, 'A': 1, 'T': 1},
            suggested_reactions=["immune_cell_formation"],
            honeyprint_config={
                "core_name": "Immune Core",
                "adapters": ["Sentinel", "Phage", "Macrophage", "Monitor"],
                "external_connections": {
                    "Monitor": "Health Dashboard",
                    "Phage": "Auto-Recovery"
                }
            },
            constraints={
                "auto_healing": True,
                "mutation_detection": True,
                "quarantine_capability": True
            }
        )
    
    async def build_component(self, blueprint_name: str, 
                            component_name: str,
                            custom_parameters: Optional[Dict[str, Any]] = None) -> BuildResult:
        """
        Build a complete molecular component from an architectural blueprint.
        
        This is the main entry point that orchestrates:
        1. Reaction processing to create the component
        2. Stability analysis
        3. Honeyprint visualization generation
        4. Registry cataloging
        5. Integration with existing components
        """
        
        print(f"👑 Queen Bee building component: {component_name} using blueprint: {blueprint_name}")
        
        if blueprint_name not in self._blueprint_library:
            return BuildResult(
                success=False,
                component_id=None,
                honeyprint_svg=None,
                stability_report=None,
                reaction_results=[],
                warnings=[f"Unknown blueprint: {blueprint_name}"]
            )
        
        blueprint = self._blueprint_library[blueprint_name]
        custom_parameters = custom_parameters or {}
        
        # Step 0: Validate against Beekeeper's Intent (Level 7 wisdom)
        intent_validation = self._validate_beekeeper_intent(blueprint, component_name, custom_parameters)
        if not intent_validation["approved"]:
            return BuildResult(
                success=False,
                component_id=None,
                honeyprint_svg=None,
                stability_report=None,
                reaction_results=[],
                warnings=intent_validation["violations"],
                recommendations=intent_validation["guidance"]
            )
        
        # Step 1: Execute chemical reactions to create the component
        reaction_results = await self._execute_blueprint_reactions(blueprint, custom_parameters)
        
        if not any(result.success for result in reaction_results):
            return BuildResult(
                success=False,
                component_id=None,
                honeyprint_svg=None,
                stability_report=None,
                reaction_results=reaction_results,
                warnings=["All reactions failed - cannot create component"]
            )
        
        # Step 2: Generate molecular formula from blueprint
        molecular_formula = self._generate_formula(blueprint.required_elements)
        
        # Step 3: Perform stability analysis
        connections = self._extract_connections_from_blueprint(blueprint)
        stability_report = self.molecular_analyzer.analyze_molecular_stability(
            component_name, molecular_formula, connections
        )
        
        # Step 4: Generate honeyprint visualization
        honeyprint_svg = await self._generate_honeyprint(blueprint, component_name, custom_parameters)
        
        # Step 5: Register component in chemical registry
        molecular_component = MolecularComponent(
            name=component_name,
            molecular_formula=molecular_formula,
            element_composition=blueprint.required_elements,
            stability=self._map_stability(stability_report.stability_level),
            bond_energy=stability_report.total_bond_energy,
            creation_date=datetime.now(timezone.utc),
            created_by="queen_bee",
            description=blueprint.description,
            properties={
                "blueprint": blueprint_name,
                "stability_score": stability_report.stability_score,
                "decomposition_risk": stability_report.decomposition_risk,
                **custom_parameters
            }
        )
        
        component_id = self.chemical_registry.register_component(molecular_component)
        self._active_components[component_id] = molecular_component
        
        # Step 6: Create component files and documentation
        await self._create_component_files(component_name, blueprint, honeyprint_svg, stability_report)
        
        # Step 7: Generate recommendations
        recommendations = self._generate_recommendations(blueprint, stability_report, reaction_results)
        
        # Step 8: Update system metrics (including wisdom alignment)
        wisdom_score = intent_validation.get("wisdom_score", 0.5)
        self._update_system_health(stability_report, wisdom_score)
        
        build_result = BuildResult(
            success=True,
            component_id=component_id,
            honeyprint_svg=honeyprint_svg,
            stability_report=stability_report,
            reaction_results=reaction_results,
            recommendations=recommendations
        )
        
        # Record build history
        self._build_history.append((datetime.now(timezone.utc), build_result))
        
        print(f"✅ Component {component_name} built successfully!")
        print(f"   Stability: {stability_report.stability_level.value}")
        print(f"   Score: {stability_report.stability_score:.1f}/100")
        print(f"   Component ID: {component_id}")
        
        return build_result
    
    async def _execute_blueprint_reactions(self, blueprint: ArchitecturalBlueprint,
                                         custom_parameters: Dict[str, Any]) -> List[ReactionResult]:
        """Execute all reactions specified in the blueprint"""
        results = []
        
        # Prepare reactants based on required elements
        available_reactants = []
        for element, count in blueprint.required_elements.items():
            available_reactants.extend([element] * count)
        
        # Add custom reactants if specified
        if "additional_reactants" in custom_parameters:
            available_reactants.extend(custom_parameters["additional_reactants"])
        
        # Execute each suggested reaction
        for reaction_name in blueprint.suggested_reactions:
            if reaction_name in self.reaction_engine._known_reactions:
                reaction = self.reaction_engine._known_reactions[reaction_name]
                
                # Use royal jelly as default catalyst
                catalysts = custom_parameters.get("catalysts", ["royal_jelly"])
                
                result = self.reaction_engine.execute_reaction(
                    reaction,
                    available_reactants,
                    catalysts,
                    temperature=custom_parameters.get("temperature", 298.0),
                    pressure=custom_parameters.get("pressure", 1.0)
                )
                
                results.append(result)
        
        return results
    
    def _validate_beekeeper_intent(self, blueprint: ArchitecturalBlueprint, 
                                 component_name: str, 
                                 custom_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the build against Beekeeper's Intent (Level 7 of the Hive).
        
        This method ensures that every component built serves the greater purpose
        and follows the philosophical principles laid down by the Beekeeper.
        """
        violations = []
        guidance = []
        wisdom_score = 0.0
        
        # Check component purpose clarity
        if not blueprint.description or len(blueprint.description) < 10:
            violations.append("❌ Component lacks clear purpose - violates 'Every component must have a clear purpose'")
        else:
            wisdom_score += 0.2
            
        # Check against sacred constraints
        for constraint in self.beekeeper_wisdom.sacred_constraints:
            if "ATCG genetic code integrity" in constraint:
                # Validate ATCG element ratios are reasonable
                total_elements = sum(blueprint.required_elements.values())
                if total_elements == 0:
                    violations.append(f"❌ Empty molecular formula violates: {constraint}")
                else:
                    wisdom_score += 0.15
            
            elif "Sacred Codons must be validated" in constraint:
                # Check if blueprint reactions map to Sacred Codons
                has_sacred_reactions = any(
                    reaction_name.endswith("_codon") 
                    for reaction_name in blueprint.suggested_reactions
                )
                if blueprint.suggested_reactions and not has_sacred_reactions:
                    violations.append(f"⚠️ No Sacred Codon reactions found - consider: {constraint}")
                else:
                    wisdom_score += 0.15
        
        # Check architectural values alignment
        if blueprint.beekeeper_intent:
            intent = blueprint.beekeeper_intent
            
            # Validate value alignment with Queen's wisdom
            for value_name, blueprint_weight in intent.values.items():
                queen_weight = self.beekeeper_wisdom.values.get(value_name, 0.5)
                if abs(blueprint_weight - queen_weight) > 0.3:
                    guidance.append(
                        f"💡 {value_name.title()} weight ({blueprint_weight:.1f}) differs from Queen's wisdom ({queen_weight:.1f})"
                    )
                else:
                    wisdom_score += 0.1
        
        # Check naming conventions (beauty and clarity)
        if not component_name[0].isupper():
            violations.append("❌ Component name should start with capital letter - violates beauty principle")
        
        if "_" in component_name and not component_name.replace("_", "").isalnum():
            violations.append("❌ Component name contains special characters - violates simplicity principle")
        
        # Check for organic growth patterns
        existing_similar = [
            comp for comp_id, comp in self._active_components.items()
            if comp.name.lower().startswith(component_name.lower()[:4])
        ]
        if len(existing_similar) > 3:
            guidance.append(
                f"🌱 Multiple similar components detected - ensure organic growth, not chaotic proliferation"
            )
        
        # Calculate final approval
        max_violations_allowed = 1 if custom_parameters.get("force_build") else 0
        approved = len(violations) <= max_violations_allowed
        
        # Add wisdom guidance
        if wisdom_score >= 0.8:
            guidance.append("✨ Excellent alignment with Beekeeper's wisdom!")
        elif wisdom_score >= 0.6:
            guidance.append("📈 Good alignment - minor improvements possible")
        else:
            guidance.append("📚 Consider reviewing the Beekeeper's principles for better alignment")
        
        # Add mission-specific guidance
        if approved and blueprint.beekeeper_intent:
            guidance.append(f"🎯 Mission alignment: {blueprint.beekeeper_intent.mission}")
        
        return {
            "approved": approved,
            "violations": violations,
            "guidance": guidance,
            "wisdom_score": wisdom_score,
            "philosophy": self.beekeeper_wisdom.philosophy
        }
    
    async def _generate_honeyprint(self, blueprint: ArchitecturalBlueprint,
                                 component_name: str,
                                 custom_parameters: Dict[str, Any]) -> str:
        """Generate honeyprint SVG visualization for the component"""
        
        config = blueprint.honeyprint_config
        
        # Create the molecular structure
        if "adapters" in config:
            molecule = self.honeyprint_generator.create_hexagonal_molecule(
                config.get("core_name", component_name),
                config["adapters"]
            )
            
            # Add external connections if specified
            if "external_connections" in config:
                molecule = self.honeyprint_generator.add_external_connections(
                    molecule, config["external_connections"]
                )
        else:
            # Create a simple molecule structure
            molecule = HoneyprintMolecule(name=component_name)
            # Add basic atoms based on element composition
            # (This would be more sophisticated in a real implementation)
        
        # Generate the SVG
        svg_content = self.honeyprint_generator.generate_svg(molecule)
        
        return svg_content
    
    async def _create_component_files(self, component_name: str,
                                    blueprint: ArchitecturalBlueprint,
                                    honeyprint_svg: str,
                                    stability_report: MolecularStabilityReport):
        """Create the physical files for the component"""
        
        component_dir = self.hive_root / component_name
        component_dir.mkdir(parents=True, exist_ok=True)
        
        # Create honeyprint visualization
        honeyprint_path = component_dir / "honeyprint.svg"
        with open(honeyprint_path, 'w') as f:
            f.write(honeyprint_svg)
        
        # Create component metadata
        metadata = {
            "component_name": component_name,
            "blueprint": blueprint.name,
            "creation_date": datetime.now(timezone.utc).isoformat(),
            "molecular_formula": self._generate_formula(blueprint.required_elements),
            "stability": {
                "level": stability_report.stability_level.value,
                "score": stability_report.stability_score,
                "recommendations": stability_report.recommendations
            },
            "architecture": {
                "required_elements": blueprint.required_elements,
                "constraints": blueprint.constraints,
                "description": blueprint.description
            }
        }
        
        metadata_path = component_dir / "component.yaml"
        with open(metadata_path, 'w') as f:
            yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
        
        # Create README with architectural documentation
        readme_content = f"""# {component_name}

## Molecular Architecture

**Blueprint**: {blueprint.name}  
**Stability**: {stability_report.stability_level.value} ({stability_report.stability_score:.1f}/100)  
**Formula**: {self._generate_formula(blueprint.required_elements)}  
**Bond Energy**: {stability_report.total_bond_energy:.1f} kJ/mol  

## Description

{blueprint.description}

## Architecture Diagram

![Honeyprint](honeyprint.svg)

## Stability Analysis

{chr(10).join(f'- {rec}' for rec in stability_report.recommendations)}

## Generated by Queen Bee 👑

This component was generated using the Hive Molecular Architecture system.
Creation Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
        
        readme_path = component_dir / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        print(f"📁 Component files created in: {component_dir}")
    
    def _generate_formula(self, elements: Dict[str, int]) -> str:
        """Generate molecular formula from element composition"""
        formula_parts = []
        for element in ['A', 'T', 'C', 'G']:  # ATCG order
            if element in elements and elements[element] > 0:
                count = elements[element]
                if count == 1:
                    formula_parts.append(element)
                else:
                    formula_parts.append(f"{element}{count}")
        
        return "".join(formula_parts)
    
    def _extract_connections_from_blueprint(self, blueprint: ArchitecturalBlueprint) -> List[Tuple[str, str]]:
        """Extract connection information from blueprint for stability analysis"""
        connections = []
        
        config = blueprint.honeyprint_config
        if "adapters" in config:
            core_name = config.get("core_name", "Core")
            for adapter in config["adapters"]:
                connections.append((core_name, adapter))
        
        if "external_connections" in config:
            for adapter, external in config["external_connections"].items():
                connections.append((adapter, external))
        
        return connections
    
    def _map_stability(self, arch_stability: ArchitecturalStability) -> ComponentStability:
        """Map architectural stability to component stability"""
        mapping = {
            ArchitecturalStability.RADICAL: ComponentStability.EXPERIMENTAL,
            ArchitecturalStability.UNSTABLE: ComponentStability.EXPERIMENTAL,
            ArchitecturalStability.STABLE: ComponentStability.STABLE,
            ArchitecturalStability.AROMATIC: ComponentStability.STABLE,
            ArchitecturalStability.INERT: ComponentStability.DEPRECATED
        }
        return mapping.get(arch_stability, ComponentStability.EXPERIMENTAL)
    
    def _generate_recommendations(self, blueprint: ArchitecturalBlueprint,
                                stability_report: MolecularStabilityReport,
                                reaction_results: List[ReactionResult]) -> List[str]:
        """Generate intelligent recommendations for the component"""
        recommendations = []
        
        # From stability analysis
        recommendations.extend(stability_report.recommendations)
        
        # From reaction analysis
        failed_reactions = [r for r in reaction_results if not r.success]
        if failed_reactions:
            recommendations.append(f"⚠️ {len(failed_reactions)} reactions failed - consider alternative synthesis routes")
        
        # Blueprint-specific recommendations
        if stability_report.stability_score < 70:
            recommendations.append("📐 Consider adding more connections for improved stability")
        
        if blueprint.target_stability == ArchitecturalStability.AROMATIC and stability_report.stability_level != ArchitecturalStability.AROMATIC:
            recommendations.append("🔄 Target aromatic stability not achieved - review hexagonal architecture implementation")
        
        return recommendations
    
    def _update_system_health(self, stability_report: MolecularStabilityReport, 
                             wisdom_score: float = None):
        """Update overall system health metrics including Intent alignment"""
        # Update running averages
        self._system_health["stability_score"] = (
            self._system_health["stability_score"] * 0.9 + 
            stability_report.stability_score * 0.1
        )
        
        # Update aromatic ratio
        if stability_report.stability_level == ArchitecturalStability.AROMATIC:
            self._system_health["aromatic_ratio"] = min(1.0, self._system_health["aromatic_ratio"] + 0.05)
        
        # Update wisdom alignment if provided
        if wisdom_score is not None:
            self._system_health["wisdom_alignment"] = (
                self._system_health["wisdom_alignment"] * 0.9 + 
                wisdom_score * 0.1
            )
        
        # Update purpose clarity based on component descriptions
        if hasattr(stability_report, 'description') and stability_report.description:
            clarity_score = min(1.0, len(stability_report.description) / 100.0)
            self._system_health["purpose_clarity"] = (
                self._system_health["purpose_clarity"] * 0.9 + 
                clarity_score * 0.1
            )
        
        # Update beauty index based on stability and naming
        beauty_factors = [
            stability_report.stability_score / 100.0,
            1.0 if stability_report.stability_level == ArchitecturalStability.AROMATIC else 0.5,
            len(stability_report.recommendations) == 0 and 1.0 or 0.7  # Fewer recommendations = more beautiful
        ]
        beauty_score = sum(beauty_factors) / len(beauty_factors)
        self._system_health["beauty_index"] = (
            self._system_health["beauty_index"] * 0.9 + 
            beauty_score * 0.1
        )
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health and metrics"""
        total_components = len(self._active_components)
        total_builds = len(self._build_history)
        recent_builds = [b for t, b in self._build_history if (datetime.now(timezone.utc) - t).days < 7]
        
        return {
            "health_metrics": self._system_health,
            "component_count": total_components,
            "total_builds": total_builds,
            "recent_builds": len(recent_builds),
            "success_rate": sum(1 for b in recent_builds if b.success) / max(1, len(recent_builds)),
            "average_stability": sum(b.stability_report.stability_score for b in recent_builds if b.stability_report) / max(1, len(recent_builds)),
            "available_blueprints": list(self._blueprint_library.keys())
        }
    
    def get_blueprint_catalog(self) -> Dict[str, Dict[str, Any]]:
        """Get catalog of available architectural blueprints"""
        catalog = {}
        for name, blueprint in self._blueprint_library.items():
            catalog[name] = {
                "name": blueprint.name,
                "description": blueprint.description,
                "stability": blueprint.target_stability.value,
                "elements": blueprint.required_elements,
                "reactions": blueprint.suggested_reactions,
                "constraints": blueprint.constraints
            }
        return catalog
    
    def get_beekeeper_wisdom(self) -> BeekeeperWisdom:
        """Get the Beekeeper's Intent that guides all architectural decisions"""
        return self.beekeeper_wisdom
    
    def evaluate_wisdom_alignment(self, component_name: str) -> Dict[str, Any]:
        """Evaluate how well a component aligns with the Beekeeper's wisdom"""
        if component_name not in [comp.name for comp in self._active_components.values()]:
            return {"error": "Component not found"}
        
        component = next(comp for comp in self._active_components.values() if comp.name == component_name)
        
        # Evaluate against principles
        principle_scores = {}
        for principle in self.beekeeper_wisdom.principles:
            if "clear purpose" in principle.lower():
                score = 1.0 if component.description and len(component.description) > 20 else 0.3
            elif "simplicity" in principle.lower():
                score = 1.0 if component.molecular_formula.count('A') <= 2 else 0.6
            elif "self-healing" in principle.lower():
                score = 1.0 if component.stability.value in ["stable", "aromatic"] else 0.4
            else:
                score = 0.7  # Default neutral score
            
            principle_scores[principle] = score
        
        overall_alignment = sum(principle_scores.values()) / len(principle_scores)
        
        return {
            "component": component_name,
            "overall_alignment": overall_alignment,
            "principle_scores": principle_scores,
            "mission_alignment": self.beekeeper_wisdom.mission,
            "philosophy": self.beekeeper_wisdom.philosophy,
            "recommendations": [
                f"Consider improving: {principle}" 
                for principle, score in principle_scores.items() 
                if score < 0.6
            ]
        }

# Example usage and testing
async def main():
    """Example of using the Queen Bee system"""
    queen = QueenBee()
    
    print("👑 Queen Bee System Demo\n")
    
    # Show available blueprints
    catalog = queen.get_blueprint_catalog()
    print("📋 Available Blueprints:")
    for name, info in catalog.items():
        print(f"  - {name}: {info['description']}")
    
    # Build a hexagonal core component
    print("\n🔬 Building Hexagonal Core Component...")
    result = await queen.build_component(
        "hexagonal_core", 
        "UserService",
        {"temperature": 310.0, "catalysts": ["royal_jelly", "beekeeper_wisdom"]}
    )
    
    if result.success:
        print(f"✅ Build successful! Component ID: {result.component_id}")
        print(f"   Stability: {result.stability_report.stability_level.value}")
        print(f"   Recommendations: {len(result.recommendations)}")
    else:
        print(f"❌ Build failed: {result.warnings}")
    
    # Show system health
    health = queen.get_system_health()
    print(f"\n📊 System Health:")
    print(f"  Overall Stability: {health['health_metrics']['stability_score']:.1f}")
    print(f"  Components Built: {health['component_count']}")
    print(f"  Success Rate: {health['success_rate']:.2%}")

if __name__ == "__main__":
    asyncio.run(main())