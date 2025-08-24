"""
Hive Molecular Architecture Framework - Bio/Sci Molecular Engineering

This module implements molecular-level architecture where software components
can form stable molecular structures through chemical bonds. Components combine
to create molecules with emergent properties that exceed their individual 
capabilities, following bio/sci nature/orgs philosophy.

Key Bio/Sci Principles:
- Components bond to form stable molecular structures
- Molecules have emergent properties beyond individual components
- Molecular geometry affects functionality and stability  
- Chemical equilibrium maintains system balance
- Molecular evolution through beneficial structural changes
"""

from typing import Dict, List, Optional, Tuple, Set, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid
import math
import numpy as np
from datetime import datetime, timezone
from collections import defaultdict, deque
import threading

from .chemical_periodic_system import (
    ChemicalElement, BondType, ToxicityLevel,
    PeriodicTableSystem, get_periodic_table_system
)
from .chemical_bond_engine import (
    ChemicalBond, BondState, ChemicalBondEngine, get_chemical_bond_engine
)


class MolecularGeometry(Enum):
    """3D molecular geometry types"""
    
    LINEAR = "linear"                    # 2 atoms, 180°
    BENT = "bent"                       # 3 atoms, <180° 
    TRIGONAL_PLANAR = "trigonal_planar" # 3 atoms, 120°
    TETRAHEDRAL = "tetrahedral"         # 4 atoms, 109.5°
    TRIGONAL_BIPYRAMIDAL = "trigonal_bipyramidal"  # 5 atoms
    OCTAHEDRAL = "octahedral"           # 6 atoms, 90°
    PENTAGONAL_BIPYRAMIDAL = "pentagonal_bipyramidal"  # 7 atoms
    COMPLEX_3D = "complex_3d"           # More than 7 atoms


class MolecularState(Enum):
    """States of molecular structures"""
    
    FORMING = "forming"          # Molecule in assembly process
    STABLE = "stable"           # Fully formed, stable molecule
    EXCITED = "excited"         # Higher energy state
    TRANSITION = "transition"   # Undergoing structural change
    DISSOCIATING = "dissociating"  # Breaking apart
    CATALYTIC = "catalytic"     # Acting as catalyst
    REACTIVE = "reactive"       # Ready for reactions


class MolecularFunction(Enum):
    """Functional roles of molecules"""
    
    STRUCTURAL = "structural"           # Provides structure/framework
    CATALYTIC = "catalytic"            # Accelerates reactions
    TRANSPORT = "transport"            # Moves components/data
    STORAGE = "storage"                # Stores information/energy
    SIGNALING = "signaling"            # Communication between components
    PROTECTIVE = "protective"          # Defensive/shielding function
    REGULATORY = "regulatory"          # Controls other components
    METABOLIC = "metabolic"           # Energy conversion/processing


@dataclass  
class MolecularBond:
    """Enhanced bond with molecular geometry information"""
    
    chemical_bond: ChemicalBond
    bond_angle: float = 109.5           # Degrees
    dihedral_angle: float = 0.0         # Degrees (for 3D structure)
    bond_order: int = 1                 # Single, double, triple bonds
    
    # Geometric properties
    x_coordinate: float = 0.0
    y_coordinate: float = 0.0  
    z_coordinate: float = 0.0
    
    # Molecular orbital information
    hybridization: str = "sp3"          # sp, sp2, sp3, sp3d, sp3d2
    electron_density: float = 1.0       # Relative electron density
    polarity: float = 0.0               # Bond polarity (-1 to 1)


@dataclass
class SoftwareMolecule:
    """
    Represents a molecular structure formed by software components
    
    A molecule is a stable collection of components bonded together
    that exhibits emergent properties and behaviors.
    """
    
    molecule_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    molecular_formula: str = ""          # Like "C6H12O6" for glucose
    
    # Component composition
    component_elements: List[ChemicalElement] = field(default_factory=list)
    component_ids: List[str] = field(default_factory=list)
    molecular_bonds: List[MolecularBond] = field(default_factory=list)
    
    # Molecular properties
    molecular_weight: float = 0.0        # Sum of atomic weights
    geometry: MolecularGeometry = MolecularGeometry.LINEAR
    state: MolecularState = MolecularState.FORMING
    primary_function: MolecularFunction = MolecularFunction.STRUCTURAL
    
    # Physical properties
    stability_score: float = 5.0         # 0.0 to 10.0
    reactivity_index: float = 5.0        # 0.0 to 10.0
    polarity: float = 0.0               # -10.0 to 10.0 (negative = electron rich)
    solubility: float = 5.0             # 0.0 to 10.0
    
    # Thermodynamic properties
    formation_energy: float = 0.0        # kJ/mol
    entropy: float = 100.0              # J/(mol·K)
    heat_capacity: float = 50.0          # J/(mol·K)
    
    # Bio/Sci properties
    biological_activity: float = 5.0     # 0.0 to 10.0
    evolutionary_fitness: float = 6.0    # 0.0 to 10.0
    adaptive_capacity: float = 7.0       # 0.0 to 10.0
    
    # Molecular behavior
    diffusion_rate: float = 1.0          # Relative diffusion rate
    binding_affinity: Dict[str, float] = field(default_factory=dict)
    catalytic_sites: List[Tuple[int, str]] = field(default_factory=list)  # (atom_index, site_type)
    
    # System integration
    creation_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_interaction: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    interaction_count: int = 0
    
    def calculate_molecular_weight(self) -> float:
        """Calculate total molecular weight from constituent elements"""
        
        total_weight = sum(element.atomic_mass for element in self.component_elements)
        self.molecular_weight = total_weight
        return total_weight
    
    def determine_geometry(self) -> MolecularGeometry:
        """Determine molecular geometry based on number of components and bonds"""
        
        num_atoms = len(self.component_elements)
        num_bonds = len(self.molecular_bonds)
        
        if num_atoms == 2:
            self.geometry = MolecularGeometry.LINEAR
        elif num_atoms == 3:
            if num_bonds == 2:
                self.geometry = MolecularGeometry.BENT
            else:
                self.geometry = MolecularGeometry.TRIGONAL_PLANAR
        elif num_atoms == 4:
            self.geometry = MolecularGeometry.TETRAHEDRAL
        elif num_atoms == 5:
            self.geometry = MolecularGeometry.TRIGONAL_BIPYRAMIDAL
        elif num_atoms == 6:
            self.geometry = MolecularGeometry.OCTAHEDRAL
        elif num_atoms == 7:
            self.geometry = MolecularGeometry.PENTAGONAL_BIPYRAMIDAL
        else:
            self.geometry = MolecularGeometry.COMPLEX_3D
        
        return self.geometry
    
    def calculate_stability(self) -> float:
        """Calculate overall molecular stability"""
        
        if not self.molecular_bonds:
            return 0.0
        
        # Average bond stability
        bond_stabilities = []
        for mol_bond in self.molecular_bonds:
            bond_stability = mol_bond.chemical_bond.calculate_bond_stability()
            bond_stabilities.append(bond_stability)
        
        avg_bond_stability = sum(bond_stabilities) / len(bond_stabilities)
        
        # Geometry stability factor
        geometry_factors = {
            MolecularGeometry.TETRAHEDRAL: 1.2,
            MolecularGeometry.OCTAHEDRAL: 1.1,
            MolecularGeometry.LINEAR: 0.9,
            MolecularGeometry.BENT: 0.8,
            MolecularGeometry.COMPLEX_3D: 0.7
        }
        
        geometry_factor = geometry_factors.get(self.geometry, 1.0)
        
        # Calculate final stability
        stability = avg_bond_stability * geometry_factor
        
        # Size penalty for very large molecules
        size_penalty = 1.0 - (len(self.component_elements) - 4) * 0.05
        size_penalty = max(0.5, size_penalty)
        
        self.stability_score = max(0.0, min(10.0, stability * size_penalty))
        return self.stability_score
    
    def calculate_polarity(self) -> float:
        """Calculate molecular polarity based on electronegativity differences"""
        
        if len(self.component_elements) < 2:
            self.polarity = 0.0
            return 0.0
        
        total_dipole = 0.0
        
        for mol_bond in self.molecular_bonds:
            bond = mol_bond.chemical_bond
            if bond.element1 and bond.element2:
                # Electronegativity difference creates dipole
                en_diff = bond.element2.electronegativity - bond.element1.electronegativity
                
                # Consider bond length (longer bonds have weaker dipoles)
                distance_factor = 100.0 / max(bond.bond_length, 50.0)
                
                dipole_moment = en_diff * distance_factor
                total_dipole += dipole_moment
        
        # Average and scale
        self.polarity = total_dipole / len(self.molecular_bonds) if self.molecular_bonds else 0.0
        self.polarity = max(-10.0, min(10.0, self.polarity))
        
        return self.polarity
    
    def predict_reactivity(self) -> float:
        """Predict molecular reactivity based on structure and properties"""
        
        base_reactivity = 5.0
        
        # Highly polar molecules are more reactive
        polarity_factor = abs(self.polarity) * 0.2
        
        # Unstable molecules are more reactive
        instability_factor = (10.0 - self.stability_score) * 0.1
        
        # Smaller molecules are generally more reactive
        size_factor = max(0.5, 2.0 - len(self.component_elements) * 0.1)
        
        # Presence of highly reactive elements
        reactive_element_factor = 0.0
        for element in self.component_elements:
            reactive_element_factor += element.reactivity_index * 0.05
        
        self.reactivity_index = base_reactivity + polarity_factor + instability_factor + reactive_element_factor
        self.reactivity_index *= size_factor
        self.reactivity_index = max(0.0, min(10.0, self.reactivity_index))
        
        return self.reactivity_index
    
    def identify_catalytic_sites(self) -> List[Tuple[int, str]]:
        """Identify potential catalytic sites in the molecule"""
        
        catalytic_sites = []
        
        for i, element in enumerate(self.component_elements):
            # Transition metals often form catalytic sites
            if element.family.value == "transition_metals":
                catalytic_sites.append((i, "metal_center"))
            
            # High electronegativity elements can be catalytic
            elif element.electronegativity > 3.0:
                catalytic_sites.append((i, "electron_acceptor"))
            
            # Elements with lone pairs can donate electrons
            elif element.valence_electrons > 4:
                catalytic_sites.append((i, "electron_donor"))
        
        self.catalytic_sites = catalytic_sites
        return catalytic_sites
    
    def calculate_binding_affinity(self, target_molecule: 'SoftwareMolecule') -> float:
        """Calculate binding affinity with another molecule"""
        
        if not target_molecule.component_elements:
            return 0.0
        
        # Complementary polarity increases binding
        polarity_complement = 1.0 - abs(self.polarity + target_molecule.polarity) / 20.0
        polarity_complement = max(0.0, polarity_complement)
        
        # Size compatibility
        size_ratio = min(len(self.component_elements), len(target_molecule.component_elements)) / \
                    max(len(self.component_elements), len(target_molecule.component_elements))
        
        # Chemical compatibility of elements
        compatibility_score = 0.0
        compatibility_count = 0
        
        for my_element in self.component_elements:
            for their_element in target_molecule.component_elements:
                is_compatible, _ = my_element.is_compatible(their_element)
                if is_compatible:
                    bond_strength = my_element.calculate_bond_strength(their_element)
                    compatibility_score += bond_strength
                compatibility_count += 1
        
        avg_compatibility = compatibility_score / max(1, compatibility_count)
        
        # Calculate binding affinity
        binding_affinity = (polarity_complement * 3.0 + 
                          size_ratio * 2.0 + 
                          avg_compatibility) / 3.0
        
        # Store for future reference
        self.binding_affinity[target_molecule.molecule_id] = binding_affinity
        
        return binding_affinity
    
    def get_molecular_metrics(self) -> Dict[str, Any]:
        """Get comprehensive molecular metrics"""
        
        return {
            "molecule_id": self.molecule_id,
            "name": self.name,
            "molecular_formula": self.molecular_formula,
            "composition": {
                "num_components": len(self.component_elements),
                "num_bonds": len(self.molecular_bonds),
                "molecular_weight": self.molecular_weight,
                "component_types": [e.symbol for e in self.component_elements]
            },
            "geometry": {
                "shape": self.geometry.value,
                "state": self.state.value,
                "primary_function": self.primary_function.value
            },
            "properties": {
                "stability_score": self.stability_score,
                "reactivity_index": self.reactivity_index,
                "polarity": self.polarity,
                "solubility": self.solubility,
                "biological_activity": self.biological_activity
            },
            "thermodynamics": {
                "formation_energy": self.formation_energy,
                "entropy": self.entropy,
                "heat_capacity": self.heat_capacity
            },
            "catalysis": {
                "num_catalytic_sites": len(self.catalytic_sites),
                "catalytic_sites": self.catalytic_sites
            },
            "interactions": {
                "interaction_count": self.interaction_count,
                "binding_affinities": dict(self.binding_affinity),
                "age_seconds": (datetime.now(timezone.utc) - self.creation_time).total_seconds()
            }
        }


class MolecularArchitectureEngine:
    """
    Molecular Architecture Engine for the Hive System
    
    Manages the formation, evolution, and interactions of molecular 
    structures built from software components following chemical principles.
    """
    
    def __init__(self):
        self.periodic_system = get_periodic_table_system()
        self.bond_engine = get_chemical_bond_engine()
        
        # Molecular management
        self.active_molecules: Dict[str, SoftwareMolecule] = {}
        self.molecular_templates: Dict[str, Dict[str, Any]] = {}
        self.molecular_reactions: Dict[str, List[str]] = defaultdict(list)
        
        # Component tracking
        self.component_molecules: Dict[str, str] = {}  # component_id -> molecule_id
        self.free_components: Set[str] = set()
        
        # Performance tracking
        self.molecules_formed: int = 0
        self.molecules_dissociated: int = 0
        self.successful_reactions: int = 0
        self.failed_reactions: int = 0
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Initialize common molecular templates
        self._initialize_molecular_templates()
    
    def _initialize_molecular_templates(self):
        """Initialize common molecular structure templates"""
        
        # Water-like structure (H-O-H) - Simple bridge pattern
        self.molecular_templates["bridge_molecule"] = {
            "elements": ["H", "O", "H"],
            "component_types": ["event", "connector", "event"], 
            "bonds": [(0, 1), (1, 2)],
            "geometry": MolecularGeometry.BENT,
            "function": MolecularFunction.TRANSPORT,
            "description": "Simple bridge connecting two components"
        }
        
        # Methane-like structure (C with 4 H) - Central hub pattern  
        self.molecular_templates["hub_molecule"] = {
            "elements": ["C", "H", "H", "H", "H"],
            "component_types": ["aggregate", "event", "event", "event", "event"],
            "bonds": [(0, 1), (0, 2), (0, 3), (0, 4)],
            "geometry": MolecularGeometry.TETRAHEDRAL,
            "function": MolecularFunction.STRUCTURAL,
            "description": "Central hub managing multiple connections"
        }
        
        # Benzene-like structure - Stable ring pattern
        self.molecular_templates["ring_molecule"] = {
            "elements": ["C", "C", "C", "C", "C", "C"],
            "component_types": ["aggregate", "aggregate", "aggregate", "aggregate", "aggregate", "aggregate"],
            "bonds": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)],
            "geometry": MolecularGeometry.COMPLEX_3D,
            "function": MolecularFunction.STRUCTURAL,
            "description": "Stable circular structure with high stability"
        }
        
        # ATP-like energy molecule - Complex energy storage
        self.molecular_templates["energy_molecule"] = {
            "elements": ["N", "C", "P", "P", "P", "O", "O", "O"],
            "component_types": ["validator", "aggregate", "processor", "processor", "processor", "connector", "connector", "connector"],
            "bonds": [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (3, 6), (4, 7)],
            "geometry": MolecularGeometry.COMPLEX_3D,
            "function": MolecularFunction.METABOLIC,
            "description": "High-energy molecule for system power"
        }
    
    def assemble_molecule(self, component_ids: List[str], component_types: List[str],
                         template_name: Optional[str] = None,
                         custom_bonds: Optional[List[Tuple[int, int]]] = None) -> Optional[SoftwareMolecule]:
        """Assemble a molecule from components"""
        
        with self._lock:
            if len(component_ids) != len(component_types):
                return None
            
            # Get chemical elements for components
            elements = []
            for comp_type in component_types:
                element = self.periodic_system.get_element(comp_type)
                if not element:
                    return None
                elements.append(element)
            
            # Create molecule
            molecule = SoftwareMolecule(
                name=f"Molecule_{len(self.active_molecules) + 1}",
                component_elements=elements,
                component_ids=component_ids
            )
            
            # Apply template if specified
            if template_name and template_name in self.molecular_templates:
                template = self.molecular_templates[template_name]
                molecule.geometry = template["geometry"] 
                molecule.primary_function = template["function"]
                bonds_to_create = template.get("bonds", [])
            elif custom_bonds:
                bonds_to_create = custom_bonds
            else:
                # Auto-generate bonds (connect all adjacent components)
                bonds_to_create = [(i, i+1) for i in range(len(component_ids) - 1)]
            
            # Create chemical bonds
            molecular_bonds = []
            for i, j in bonds_to_create:
                if i < len(component_ids) and j < len(component_ids):
                    chemical_bond = self.bond_engine.form_chemical_bond(
                        component_ids[i], component_types[i],
                        component_ids[j], component_types[j]
                    )
                    
                    if chemical_bond:
                        mol_bond = MolecularBond(chemical_bond=chemical_bond)
                        molecular_bonds.append(mol_bond)
            
            if not molecular_bonds:
                return None  # No bonds could be formed
            
            molecule.molecular_bonds = molecular_bonds
            
            # Calculate molecular properties
            molecule.calculate_molecular_weight()
            molecule.determine_geometry()
            molecule.calculate_stability()
            molecule.calculate_polarity()
            molecule.predict_reactivity()
            molecule.identify_catalytic_sites()
            
            # Generate molecular formula
            element_counts = {}
            for element in elements:
                element_counts[element.symbol] = element_counts.get(element.symbol, 0) + 1
            
            formula_parts = []
            for symbol, count in sorted(element_counts.items()):
                if count == 1:
                    formula_parts.append(symbol)
                else:
                    formula_parts.append(f"{symbol}{count}")
            
            molecule.molecular_formula = "".join(formula_parts)
            
            # Set stable state
            molecule.state = MolecularState.STABLE
            
            # Store molecule
            self.active_molecules[molecule.molecule_id] = molecule
            
            # Update component tracking
            for comp_id in component_ids:
                self.component_molecules[comp_id] = molecule.molecule_id
                self.free_components.discard(comp_id)
            
            # Update metrics
            self.molecules_formed += 1
            
            return molecule
    
    def dissociate_molecule(self, molecule_id: str, force: bool = False) -> bool:
        """Break apart a molecule into individual components"""
        
        with self._lock:
            if molecule_id not in self.active_molecules:
                return False
            
            molecule = self.active_molecules[molecule_id]
            
            if not force and molecule.stability_score > 7.0:
                return False  # Too stable to dissociate naturally
            
            # Break all bonds in the molecule
            for mol_bond in molecule.molecular_bonds:
                self.bond_engine.break_chemical_bond(mol_bond.chemical_bond.bond_id, force=True)
            
            # Update component tracking
            for comp_id in molecule.component_ids:
                del self.component_molecules[comp_id]
                self.free_components.add(comp_id)
            
            # Remove molecule
            del self.active_molecules[molecule_id]
            
            # Update metrics
            self.molecules_dissociated += 1
            
            return True
    
    def catalyze_reaction(self, reactant_molecule_ids: List[str], 
                         catalyst_component_id: str, catalyst_component_type: str,
                         target_product_template: Optional[str] = None) -> Optional[SoftwareMolecule]:
        """Use a catalyst to facilitate molecular reactions"""
        
        with self._lock:
            # Get catalyst element
            catalyst_element = self.periodic_system.get_element(catalyst_component_type)
            if not catalyst_element:
                return None
            
            # Collect all components from reactant molecules
            all_component_ids = []
            all_component_types = []
            
            for mol_id in reactant_molecule_ids:
                if mol_id in self.active_molecules:
                    molecule = self.active_molecules[mol_id]
                    all_component_ids.extend(molecule.component_ids)
                    all_component_types.extend([e.name.lower() for e in molecule.component_elements])
                    
                    # Dissociate reactant molecules
                    self.dissociate_molecule(mol_id, force=True)
            
            if not all_component_ids:
                return None
            
            # Create new molecule with catalyst assistance
            product_molecule = self.assemble_molecule(
                all_component_ids, all_component_types, template_name=target_product_template
            )
            
            if product_molecule:
                # Apply catalytic effects to all bonds
                for mol_bond in product_molecule.molecular_bonds:
                    mol_bond.chemical_bond.catalyze_bond(catalyst_element, efficiency=1.8)
                
                # Mark as catalytic state temporarily
                product_molecule.state = MolecularState.CATALYTIC
                
                # Record successful reaction
                self.successful_reactions += 1
                self.molecular_reactions[catalyst_component_id].extend(reactant_molecule_ids)
            else:
                self.failed_reactions += 1
            
            return product_molecule
    
    def find_compatible_molecules(self, molecule_id: str) -> List[Tuple[str, float]]:
        """Find molecules that can interact with the given molecule"""
        
        if molecule_id not in self.active_molecules:
            return []
        
        source_molecule = self.active_molecules[molecule_id]
        compatible_molecules = []
        
        for other_id, other_molecule in self.active_molecules.items():
            if other_id != molecule_id:
                affinity = source_molecule.calculate_binding_affinity(other_molecule)
                if affinity > 0.3:  # Threshold for meaningful interaction
                    compatible_molecules.append((other_id, affinity))
        
        # Sort by affinity (highest first)
        compatible_molecules.sort(key=lambda x: x[1], reverse=True)
        return compatible_molecules
    
    def simulate_molecular_dynamics(self, time_steps: int = 10, 
                                  temperature: float = 298.15) -> Dict[str, Any]:
        """Simulate molecular dynamics over time"""
        
        dynamics_log = []
        
        with self._lock:
            for step in range(time_steps):
                step_events = []
                
                # Update all molecules
                for molecule in self.active_molecules.values():
                    old_stability = molecule.stability_score
                    new_stability = molecule.calculate_stability()
                    
                    # Check for spontaneous dissociation
                    if new_stability < 2.0 and random.random() < 0.1:
                        step_events.append({
                            "event": "spontaneous_dissociation",
                            "molecule_id": molecule.molecule_id,
                            "stability": new_stability
                        })
                        # Note: Actual dissociation would happen in next iteration
                    
                    # Check for state transitions
                    elif abs(new_stability - old_stability) > 1.0:
                        if new_stability > old_stability:
                            molecule.state = MolecularState.STABLE
                        else:
                            molecule.state = MolecularState.REACTIVE
                        
                        step_events.append({
                            "event": "state_transition", 
                            "molecule_id": molecule.molecule_id,
                            "old_stability": old_stability,
                            "new_stability": new_stability,
                            "new_state": molecule.state.value
                        })
                
                dynamics_log.append({
                    "step": step,
                    "events": step_events,
                    "active_molecules": len(self.active_molecules),
                    "temperature": temperature
                })
        
        return {
            "simulation_steps": time_steps,
            "dynamics_log": dynamics_log,
            "final_state": self.get_molecular_system_statistics()
        }
    
    def get_molecular_system_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the molecular system"""
        
        with self._lock:
            if not self.active_molecules:
                return {
                    "total_molecules": 0,
                    "system_empty": True
                }
            
            # Basic counts
            total_molecules = len(self.active_molecules)
            total_components = sum(len(mol.component_ids) for mol in self.active_molecules.values())
            total_bonds = sum(len(mol.molecular_bonds) for mol in self.active_molecules.values())
            
            # Geometry distribution
            geometry_counts = {}
            for molecule in self.active_molecules.values():
                geom = molecule.geometry.value
                geometry_counts[geom] = geometry_counts.get(geom, 0) + 1
            
            # Function distribution  
            function_counts = {}
            for molecule in self.active_molecules.values():
                func = molecule.primary_function.value
                function_counts[func] = function_counts.get(func, 0) + 1
            
            # State distribution
            state_counts = {}
            for molecule in self.active_molecules.values():
                state = molecule.state.value
                state_counts[state] = state_counts.get(state, 0) + 1
            
            # Average properties
            avg_stability = sum(mol.stability_score for mol in self.active_molecules.values()) / total_molecules
            avg_reactivity = sum(mol.reactivity_index for mol in self.active_molecules.values()) / total_molecules
            avg_polarity = sum(mol.polarity for mol in self.active_molecules.values()) / total_molecules
            avg_molecular_weight = sum(mol.molecular_weight for mol in self.active_molecules.values()) / total_molecules
            
            # Most stable and reactive molecules
            most_stable = max(self.active_molecules.values(), key=lambda m: m.stability_score)
            most_reactive = max(self.active_molecules.values(), key=lambda m: m.reactivity_index)
            
            # Catalytic capacity
            total_catalytic_sites = sum(len(mol.catalytic_sites) for mol in self.active_molecules.values())
            
            return {
                "system_overview": {
                    "total_molecules": total_molecules,
                    "total_components": total_components,
                    "total_bonds": total_bonds,
                    "free_components": len(self.free_components),
                    "molecules_formed": self.molecules_formed,
                    "molecules_dissociated": self.molecules_dissociated
                },
                "distribution_analysis": {
                    "geometry_distribution": geometry_counts,
                    "function_distribution": function_counts,
                    "state_distribution": state_counts
                },
                "average_properties": {
                    "stability_score": avg_stability,
                    "reactivity_index": avg_reactivity,
                    "polarity": avg_polarity,
                    "molecular_weight": avg_molecular_weight
                },
                "system_champions": {
                    "most_stable_molecule": {
                        "id": most_stable.molecule_id,
                        "name": most_stable.name,
                        "stability": most_stable.stability_score
                    },
                    "most_reactive_molecule": {
                        "id": most_reactive.molecule_id,
                        "name": most_reactive.name,
                        "reactivity": most_reactive.reactivity_index
                    }
                },
                "catalytic_system": {
                    "total_catalytic_sites": total_catalytic_sites,
                    "successful_reactions": self.successful_reactions,
                    "failed_reactions": self.failed_reactions,
                    "reaction_success_rate": self.successful_reactions / max(1, self.successful_reactions + self.failed_reactions)
                },
                "templates_available": len(self.molecular_templates),
                "analysis_timestamp": datetime.now(timezone.utc).isoformat()
            }


# Global molecular architecture engine instance
_global_molecular_engine = None


def get_molecular_architecture_engine() -> MolecularArchitectureEngine:
    """Get the global molecular architecture engine instance"""
    global _global_molecular_engine
    if _global_molecular_engine is None:
        _global_molecular_engine = MolecularArchitectureEngine()
    return _global_molecular_engine


def create_software_molecule(component_ids: List[str], component_types: List[str],
                           template: Optional[str] = None) -> Optional[SoftwareMolecule]:
    """Create a software molecule from components"""
    return get_molecular_architecture_engine().assemble_molecule(
        component_ids, component_types, template_name=template
    )


def analyze_molecular_system() -> Dict[str, Any]:
    """Analyze the current molecular system"""
    return get_molecular_architecture_engine().get_molecular_system_statistics()