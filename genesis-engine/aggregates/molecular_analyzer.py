#!/usr/bin/env python3
"""
The Molecular Analyzer Aggregate - Chemical Analysis for Hive Architecture
Analyzes architectural stability using chemistry principles.

This aggregate implements the "Chemical Bond System" between ATCG primitives,
determining molecular stability, bond strength, and architectural health.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from enum import Enum
import math
from datetime import datetime

class ArchitecturalStability(Enum):
    """Molecular stability levels for components"""
    RADICAL = "radical"           # Missing critical connections
    UNSTABLE = "unstable"         # Prone to decomposition
    STABLE = "stable"             # Normal operation
    AROMATIC = "aromatic"         # Extra stable, hard to change
    INERT = "inert"              # Completely unreactive

class ValenceState(Enum):
    """Valence states for ATCG elements (bonding capacity)"""
    AGGREGATE = 4      # Like Carbon - can form 4 bonds
    TRANSFORMATION = 1  # Like Hydrogen - forms 1 bond
    CONNECTOR = 2      # Like Oxygen - typically 2 bonds
    GENESIS_EVENT = 3  # Like Nitrogen - 3 bonds possible

class MutationType(Enum):
    """Types of architectural mutations (from IMMUNITY.md)"""
    CONFIGURATION_DEFECT = "configuration_defect"     # Genetic flaw - birth defect
    TRANSIENT_INFECTION = "transient_infection"       # Common cold - temporary failure
    CHRONIC_FAILURE = "chronic_failure"              # Serious illness - persistent failure
    INVARIANT_VIOLATION = "invariant_violation"      # Autoimmune disorder - internal contradiction

@dataclass
class BondAnalysis:
    """Analysis of a bond between two components"""
    bond_strength: float = 0.0
    coupling_score: float = 0.0
    stability_contribution: float = 0.0
    is_critical: bool = False
    bond_energy: float = 0.0  # Cost of breaking this bond

@dataclass
class MutationEvent:
    """Represents a detected architectural mutation (from Immune System)"""
    mutation_type: MutationType
    component_name: str
    severity: float  # 0.0 to 1.0
    description: str
    timestamp: datetime
    context: Dict[str, any] = field(default_factory=dict)
    
@dataclass
class MolecularStabilityReport:
    """Complete stability analysis of a molecular component"""
    component_name: str
    molecular_formula: str
    stability_level: ArchitecturalStability
    total_bond_energy: float
    critical_bonds: List[str]
    stability_score: float
    decomposition_risk: float
    recommendations: List[str] = field(default_factory=list)
    detected_mutations: List[MutationEvent] = field(default_factory=list)
    immune_response_required: bool = False

class MolecularAnalyzer:
    """
    Analyzes Hive architecture using chemical principles.
    Determines stability, bond strength, and architectural health.
    """
    
    def __init__(self):
        self._stability_reports: Dict[str, MolecularStabilityReport] = {}
        self._bond_analyses: Dict[Tuple[str, str], BondAnalysis] = {}
        
        # Valence electron configuration for each ATCG element
        self._valence_config = {
            'A': ValenceState.AGGREGATE.value,
            'T': ValenceState.TRANSFORMATION.value, 
            'C': ValenceState.CONNECTOR.value,
            'G': ValenceState.GENESIS_EVENT.value
        }
    
    def analyze_molecular_stability(self, component_name: str, 
                                  molecular_formula: str,
                                  connections: List[Tuple[str, str]]) -> MolecularStabilityReport:
        """
        Analyze the stability of a molecular component.
        
        Args:
            component_name: Name of the component
            molecular_formula: Chemical formula like "A2T3C1G1"
            connections: List of (from, to) connection pairs
        
        Returns:
            Detailed stability report
        """
        print(f"🧪 Analyzing molecular stability for {component_name} ({molecular_formula})")
        
        # Parse molecular formula
        atom_counts = self._parse_molecular_formula(molecular_formula)
        
        # Calculate valence satisfaction
        valence_satisfaction = self._calculate_valence_satisfaction(atom_counts, connections)
        
        # Determine stability level
        stability_level = self._determine_stability_level(valence_satisfaction, len(connections))
        
        # Calculate bond energies
        total_bond_energy = self._calculate_total_bond_energy(connections)
        
        # Identify critical bonds
        critical_bonds = self._identify_critical_bonds(connections)
        
        # Calculate stability score (0-100)
        stability_score = self._calculate_stability_score(
            valence_satisfaction, 
            stability_level, 
            total_bond_energy
        )
        
        # Assess decomposition risk
        decomposition_risk = self._assess_decomposition_risk(
            stability_level, 
            critical_bonds, 
            total_bond_energy
        )
        
        # Generate recommendations
        recommendations = self._generate_stability_recommendations(
            stability_level, 
            valence_satisfaction, 
            critical_bonds
        )
        
        # Detect architectural mutations (Immune System integration)
        detected_mutations = self._detect_architectural_mutations(
            component_name,
            molecular_formula,
            stability_level,
            valence_satisfaction,
            connections
        )
        
        # Determine if immune response is required
        immune_response_required = any(
            mutation.severity > 0.7 for mutation in detected_mutations
        )
        
        report = MolecularStabilityReport(
            component_name=component_name,
            molecular_formula=molecular_formula,
            stability_level=stability_level,
            total_bond_energy=total_bond_energy,
            critical_bonds=critical_bonds,
            stability_score=stability_score,
            decomposition_risk=decomposition_risk,
            recommendations=recommendations,
            detected_mutations=detected_mutations,
            immune_response_required=immune_response_required
        )
        
        # Cache the report
        self._stability_reports[component_name] = report
        
        print(f"✅ Stability analysis complete. Score: {stability_score:.1f}/100, Level: {stability_level.value}")
        return report
    
    def _parse_molecular_formula(self, formula: str) -> Dict[str, int]:
        """Parse molecular formula like 'A2T3C1G1' into atom counts"""
        atom_counts = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
        
        i = 0
        while i < len(formula):
            if formula[i] in atom_counts:
                element = formula[i]
                i += 1
                
                # Look for number after element
                num_str = ""
                while i < len(formula) and formula[i].isdigit():
                    num_str += formula[i]
                    i += 1
                
                count = int(num_str) if num_str else 1
                atom_counts[element] = count
            else:
                i += 1
        
        return atom_counts
    
    def _calculate_valence_satisfaction(self, atom_counts: Dict[str, int], 
                                     connections: List[Tuple[str, str]]) -> float:
        """Calculate how well valence requirements are satisfied (0-1)"""
        total_valence_needed = 0
        for element, count in atom_counts.items():
            total_valence_needed += count * self._valence_config[element]
        
        # Each connection satisfies 2 valence requirements (one for each end)
        valence_satisfied = len(connections) * 2
        
        if total_valence_needed == 0:
            return 1.0
        
        return min(1.0, valence_satisfied / total_valence_needed)
    
    def _determine_stability_level(self, valence_satisfaction: float, 
                                 connection_count: int) -> ArchitecturalStability:
        """Determine stability level based on valence satisfaction and connectivity"""
        if valence_satisfaction < 0.3:
            return ArchitecturalStability.RADICAL
        elif valence_satisfaction < 0.6:
            return ArchitecturalStability.UNSTABLE
        elif valence_satisfaction >= 0.9 and connection_count >= 6:
            return ArchitecturalStability.AROMATIC  # Like benzene - extra stable
        elif valence_satisfaction >= 0.8:
            return ArchitecturalStability.STABLE
        elif connection_count == 0:
            return ArchitecturalStability.INERT
        else:
            return ArchitecturalStability.STABLE
    
    def _calculate_total_bond_energy(self, connections: List[Tuple[str, str]]) -> float:
        """Calculate total bond energy (higher = more stable, harder to change)"""
        total_energy = 0.0
        
        for from_comp, to_comp in connections:
            # Different bond types have different energies
            if "Core" in from_comp or "Core" in to_comp:
                bond_energy = 85.0  # Strong core bonds
            elif "Event" in from_comp or "Event" in to_comp:
                bond_energy = 45.0  # Event bonds are weaker (more flexible)
            elif "Connector" in from_comp or "Connector" in to_comp:
                bond_energy = 65.0  # Medium strength adapter bonds
            else:
                bond_energy = 55.0  # Default bond strength
            
            total_energy += bond_energy
            
            # Cache bond analysis
            self._bond_analyses[(from_comp, to_comp)] = BondAnalysis(
                bond_strength=bond_energy / 100.0,
                bond_energy=bond_energy
            )
        
        return total_energy
    
    def _identify_critical_bonds(self, connections: List[Tuple[str, str]]) -> List[str]:
        """Identify bonds that are critical for stability"""
        critical = []
        
        for from_comp, to_comp in connections:
            if "Core" in from_comp or "Core" in to_comp:
                critical.append(f"{from_comp} → {to_comp}")
            elif from_comp.count("→") + to_comp.count("→") > 2:
                # Highly connected components
                critical.append(f"{from_comp} → {to_comp}")
        
        return critical
    
    def _calculate_stability_score(self, valence_satisfaction: float, 
                                 stability_level: ArchitecturalStability,
                                 total_bond_energy: float) -> float:
        """Calculate overall stability score (0-100)"""
        base_score = valence_satisfaction * 60  # 60 points for valence satisfaction
        
        # Bonus points for stability level
        stability_bonus = {
            ArchitecturalStability.RADICAL: 0,
            ArchitecturalStability.UNSTABLE: 10,
            ArchitecturalStability.STABLE: 25,
            ArchitecturalStability.AROMATIC: 35,
            ArchitecturalStability.INERT: 15
        }
        
        # Bond energy contribution (normalized)
        energy_score = min(15, total_bond_energy / 100.0)
        
        total_score = base_score + stability_bonus[stability_level] + energy_score
        return min(100.0, total_score)
    
    def _assess_decomposition_risk(self, stability_level: ArchitecturalStability,
                                 critical_bonds: List[str],
                                 total_bond_energy: float) -> float:
        """Assess risk of component decomposition (0-1)"""
        risk_factors = {
            ArchitecturalStability.RADICAL: 0.9,
            ArchitecturalStability.UNSTABLE: 0.7,
            ArchitecturalStability.STABLE: 0.2,
            ArchitecturalStability.AROMATIC: 0.05,
            ArchitecturalStability.INERT: 0.0
        }
        
        base_risk = risk_factors[stability_level]
        
        # High number of critical bonds increases risk
        critical_risk = min(0.3, len(critical_bonds) * 0.1)
        
        # Low bond energy increases risk
        energy_risk = max(0, (300 - total_bond_energy) / 1000)
        
        total_risk = min(1.0, base_risk + critical_risk + energy_risk)
        return total_risk
    
    def _generate_stability_recommendations(self, stability_level: ArchitecturalStability,
                                          valence_satisfaction: float,
                                          critical_bonds: List[str]) -> List[str]:
        """Generate recommendations to improve stability"""
        recommendations = []
        
        if stability_level == ArchitecturalStability.RADICAL:
            recommendations.extend([
                "🚨 CRITICAL: Component has unsatisfied valence requirements",
                "Add missing connections to satisfy ATCG bonding rules",
                "Consider splitting into smaller, more stable components"
            ])
        
        if stability_level == ArchitecturalStability.UNSTABLE:
            recommendations.extend([
                "⚠️ Component may be prone to architectural changes",
                "Consider adding more connections for stability",
                "Review if this component violates single responsibility principle"
            ])
        
        if valence_satisfaction < 0.7:
            recommendations.append("📐 Improve valence satisfaction by balancing ATCG ratios")
        
        if len(critical_bonds) > 5:
            recommendations.append("🔗 Too many critical bonds - consider refactoring for loose coupling")
        
        if stability_level == ArchitecturalStability.AROMATIC:
            recommendations.append("✨ Excellent stability! This component follows hexagonal architecture perfectly")
        
        return recommendations
    
    def get_periodic_table_position(self, element: str) -> Tuple[int, int]:
        """Get position of ATCG element in our custom periodic table"""
        positions = {
            'A': (1, 1),  # Period 1, Group 1 (like Hydrogen but central)
            'T': (1, 2),  # Period 1, Group 2 
            'C': (2, 1),  # Period 2, Group 1 (highly reactive)
            'G': (2, 2)   # Period 2, Group 2 (enables complex structures)
        }
        return positions.get(element, (0, 0))
    
    def predict_reaction_products(self, reactants: List[str], 
                                catalyst: Optional[str] = None) -> List[str]:
        """Predict products of architectural 'chemical reactions'"""
        products = []
        
        # Example reactions
        if "A" in reactants and "T" in reactants and "C" in reactants:
            products.append("A1T2C1")  # Basic aggregate with transformation and connector
            if catalyst == "royal_jelly":
                products.append("G1")  # Genesis event is produced
        
        if len([r for r in reactants if "C" in r]) >= 6:
            products.append("HexagonalCore")  # Forms hexagonal architecture
        
        return products
    
    def _detect_architectural_mutations(self, component_name: str,
                                      molecular_formula: str,
                                      stability_level: ArchitecturalStability,
                                      valence_satisfaction: float,
                                      connections: List[Tuple[str, str]]) -> List[MutationEvent]:
        """
        Detect architectural mutations using Immune System principles.
        
        Based on the taxonomy from IMMUNITY.md:
        - ConfigurationDefect: Birth defects in molecular structure
        - TransientInfection: Temporary connectivity issues
        - ChronicFailure: Persistent architectural problems
        - InvariantViolation: Internal molecular contradictions
        """
        mutations = []
        timestamp = datetime.now()
        
        # 1. Configuration Defect Detection (Genetic Flaws)
        atom_counts = self._parse_molecular_formula(molecular_formula)
        
        # Missing required elements
        if atom_counts['A'] == 0:
            mutations.append(MutationEvent(
                mutation_type=MutationType.CONFIGURATION_DEFECT,
                component_name=component_name,
                severity=0.9,
                description="Missing Aggregate (A) - component has no core business logic",
                timestamp=timestamp,
                context={"molecular_formula": molecular_formula}
            ))
        
        if atom_counts['C'] == 0 and len(connections) > 0:
            mutations.append(MutationEvent(
                mutation_type=MutationType.CONFIGURATION_DEFECT,
                component_name=component_name,
                severity=0.8,
                description="Missing Connector (C) but has external connections - protocol violation",
                timestamp=timestamp,
                context={"connections": len(connections)}
            ))
        
        # 2. Invariant Violation Detection (Autoimmune Disorders)
        # ATCG ratio violations
        total_atoms = sum(atom_counts.values())
        if total_atoms > 0:
            a_ratio = atom_counts['A'] / total_atoms
            if a_ratio > 0.6:  # Too many aggregates
                mutations.append(MutationEvent(
                    mutation_type=MutationType.INVARIANT_VIOLATION,
                    component_name=component_name,
                    severity=0.8,
                    description=f"Aggregate dominance violation: {a_ratio:.1%} of molecule is Aggregates (should be <60%)",
                    timestamp=timestamp,
                    context={"aggregate_ratio": a_ratio}
                ))
        
        # Valence satisfaction violations
        if valence_satisfaction < 0.3:
            mutations.append(MutationEvent(
                mutation_type=MutationType.INVARIANT_VIOLATION,
                component_name=component_name,
                severity=0.9,
                description=f"Critical valence violation: {valence_satisfaction:.1%} satisfaction (minimum 30% required)",
                timestamp=timestamp,
                context={"valence_satisfaction": valence_satisfaction}
            ))
        
        # 3. Chronic Failure Detection (Persistent Issues)
        if stability_level == ArchitecturalStability.RADICAL:
            mutations.append(MutationEvent(
                mutation_type=MutationType.CHRONIC_FAILURE,
                component_name=component_name,
                severity=0.9,
                description="Persistent instability: Component in RADICAL state",
                timestamp=timestamp,
                context={"stability_level": stability_level.value}
            ))
        
        # Too many critical bonds
        critical_bond_count = len([bond for bond in connections if "Core" in bond[0] or "Core" in bond[1]])
        if critical_bond_count > 8:
            mutations.append(MutationEvent(
                mutation_type=MutationType.CHRONIC_FAILURE,
                component_name=component_name,
                severity=0.7,
                description=f"Excessive coupling: {critical_bond_count} critical bonds (maximum 8 recommended)",
                timestamp=timestamp,
                context={"critical_bonds": critical_bond_count}
            ))
        
        # 4. Transient Infection Detection (Temporary Issues)
        if stability_level == ArchitecturalStability.UNSTABLE and valence_satisfaction > 0.6:
            mutations.append(MutationEvent(
                mutation_type=MutationType.TRANSIENT_INFECTION,
                component_name=component_name,
                severity=0.5,
                description="Temporary instability detected - may resolve with additional connections",
                timestamp=timestamp,
                context={"can_recover": True}
            ))
        
        # Genesis Event connectivity issues
        g_count = atom_counts['G']
        event_connections = len([conn for conn in connections if "Event" in conn[0] or "Event" in conn[1]])
        if g_count > 0 and event_connections == 0:
            mutations.append(MutationEvent(
                mutation_type=MutationType.TRANSIENT_INFECTION,
                component_name=component_name,
                severity=0.6,
                description="Genesis Events present but not connected - event bus isolation",
                timestamp=timestamp,
                context={"genesis_events": g_count, "event_connections": event_connections}
            ))
        
        return mutations
    
    def generate_immune_response(self, mutation: MutationEvent) -> Dict[str, any]:
        """
        Generate immune response based on mutation type (following IMMUNITY.md patterns).
        
        Returns corrective actions to be taken by Immune Cells:
        - Sentinel Cells: Detection and logging
        - Phage Cells: First response (retries, rerouting)
        - Macrophage Cells: Heavy intervention (quarantine, shutdown)
        """
        response = {
            "mutation_id": f"{mutation.component_name}_{mutation.timestamp.isoformat()}",
            "cell_type": "sentinel",  # Default to sentinel
            "actions": [],
            "priority": "low"
        }
        
        if mutation.mutation_type == MutationType.CONFIGURATION_DEFECT:
            response.update({
                "cell_type": "macrophage",
                "priority": "critical",
                "actions": [
                    "quarantine_component",
                    "prevent_startup",
                    "alert_beekeeper",
                    "log_configuration_error"
                ]
            })
        
        elif mutation.mutation_type == MutationType.INVARIANT_VIOLATION:
            response.update({
                "cell_type": "macrophage", 
                "priority": "critical",
                "actions": [
                    "isolate_aggregate",
                    "halt_operations",
                    "log_critical_alert",
                    "trigger_emergency_response"
                ]
            })
        
        elif mutation.mutation_type == MutationType.CHRONIC_FAILURE:
            response.update({
                "cell_type": "macrophage",
                "priority": "high",
                "actions": [
                    "activate_circuit_breaker",
                    "reroute_traffic",
                    "prepare_apoptosis",
                    "gather_diagnostics"
                ]
            })
        
        elif mutation.mutation_type == MutationType.TRANSIENT_INFECTION:
            response.update({
                "cell_type": "phage",
                "priority": "medium", 
                "actions": [
                    "retry_with_backoff",
                    "check_external_dependencies",
                    "monitor_recovery",
                    "escalate_if_persistent"
                ]
            })
        
        return response

# Example usage
if __name__ == "__main__":
    analyzer = MolecularAnalyzer()
    
    # Analyze a sample component
    connections = [
        ("Core", "REST_Adapter"),
        ("Core", "SQL_Adapter"), 
        ("REST_Adapter", "User"),
        ("SQL_Adapter", "Database")
    ]
    
    report = analyzer.analyze_molecular_stability(
        "OrderService",
        "A1T2C2G1",
        connections
    )
    
    print(f"\n🧪 Analysis Results:")
    print(f"Stability: {report.stability_level.value}")
    print(f"Score: {report.stability_score:.1f}/100")
    print(f"Decomposition Risk: {report.decomposition_risk:.2f}")
    print(f"Recommendations: {len(report.recommendations)} items")
    
    # Show immune system analysis
    if report.detected_mutations:
        print(f"\n🦠 Immune System Analysis:")
        print(f"Mutations detected: {len(report.detected_mutations)}")
        print(f"Immune response required: {report.immune_response_required}")
        
        for mutation in report.detected_mutations:
            print(f"  • {mutation.mutation_type.value}: {mutation.description}")
            
            # Generate immune response
            response = analyzer.generate_immune_response(mutation)
            print(f"    → {response['cell_type']} cell response: {response['priority']} priority")
    else:
        print(f"\n✅ Immune System: No mutations detected - component is healthy!")