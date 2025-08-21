#!/usr/bin/env python3
"""
The Honeyprint Generator - A Molecular Visualization Transformation
Creates beautiful SVG molecular diagrams of Hive architecture components.

Inspired by benzene chemistry, each component becomes a molecular structure
with bonds representing architectural relationships.
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum

class MolecularElement(Enum):
    """The ATCG elements of our molecular architecture"""
    AGGREGATE = "A"      # Carbon-like: forms the backbone
    TRANSFORMATION = "T"  # Hydrogen-like: simple, ubiquitous
    CONNECTOR = "C"       # Oxygen-like: highly reactive, forms bonds
    GENESIS_EVENT = "G"   # Nitrogen-like: enables complex structures

class BondType(Enum):
    """Types of molecular bonds between components"""
    SINGLE = 1    # Simple dependency
    DOUBLE = 2    # Strong coupling
    AROMATIC = 3  # Hexagonal architecture bond
    IONIC = 4     # Event-driven connection

@dataclass
class MolecularAtom:
    """An atomic component in our molecular architecture"""
    element: MolecularElement
    name: str
    x: float = 0.0
    y: float = 0.0
    radius: float = 20.0
    color: str = "#f1c40f"
    
    def __post_init__(self):
        # Set element-specific properties
        if self.element == MolecularElement.AGGREGATE:
            self.color = "#fff3cd"
            self.radius = 40.0
        elif self.element == MolecularElement.TRANSFORMATION:
            self.color = "#fff9e6" 
            self.radius = 25.0
        elif self.element == MolecularElement.CONNECTOR:
            self.color = "#f1c40f"
            self.radius = 25.0
        elif self.element == MolecularElement.GENESIS_EVENT:
            self.color = "#ffeb99"
            self.radius = 30.0

@dataclass
class MolecularBond:
    """A bond between two molecular components"""
    from_atom: MolecularAtom
    to_atom: MolecularAtom
    bond_type: BondType = BondType.SINGLE
    strength: float = 1.0
    
    def get_svg_path(self) -> str:
        """Generate SVG path for the bond"""
        if self.bond_type == BondType.AROMATIC:
            # Hexagonal aromatic bond (dashed)
            return f'<line x1="{self.from_atom.x}" y1="{self.from_atom.y}" x2="{self.to_atom.x}" y2="{self.to_atom.y}" class="aromatic-bond" stroke-dasharray="5,5"/>'
        elif self.bond_type == BondType.DOUBLE:
            # Double bond (two parallel lines)
            dx = self.to_atom.x - self.from_atom.x
            dy = self.to_atom.y - self.from_atom.y
            length = math.sqrt(dx*dx + dy*dy)
            unit_x, unit_y = dx/length, dy/length
            perp_x, perp_y = -unit_y * 3, unit_x * 3
            
            return f'''<line x1="{self.from_atom.x + perp_x}" y1="{self.from_atom.y + perp_y}" x2="{self.to_atom.x + perp_x}" y2="{self.to_atom.y + perp_y}" class="bond"/>
                      <line x1="{self.from_atom.x - perp_x}" y1="{self.from_atom.y - perp_y}" x2="{self.to_atom.x - perp_x}" y2="{self.to_atom.y - perp_y}" class="bond"/>'''
        else:
            # Single bond
            return f'<line x1="{self.from_atom.x}" y1="{self.from_atom.y}" x2="{self.to_atom.x}" y2="{self.to_atom.y}" class="bond"/>'

@dataclass 
class HoneyprintMolecule:
    """A complete molecular structure representing a Hive component"""
    name: str
    atoms: List[MolecularAtom] = field(default_factory=list)
    bonds: List[MolecularBond] = field(default_factory=list)
    molecular_formula: str = ""
    
    def calculate_formula(self) -> str:
        """Calculate molecular formula like C6H12O6"""
        element_counts = {}
        for atom in self.atoms:
            element = atom.element.value
            element_counts[element] = element_counts.get(element, 0) + 1
        
        # Order by ATCG convention
        formula_parts = []
        for element in ['A', 'T', 'C', 'G']:
            if element in element_counts:
                count = element_counts[element]
                if count > 1:
                    formula_parts.append(f"{element}₂" if count == 2 else f"{element}{count}")
                else:
                    formula_parts.append(element)
        
        self.molecular_formula = "".join(formula_parts)
        return self.molecular_formula

class HoneyprintGenerator:
    """Generates beautiful SVG molecular diagrams for Hive architecture"""
    
    def __init__(self, width: int = 600, height: int = 500):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
    
    def create_hexagonal_molecule(self, core_name: str, adapters: List[str]) -> HoneyprintMolecule:
        """Create a benzene-like hexagonal molecular structure"""
        molecule = HoneyprintMolecule(name=f"{core_name}_hexagon")
        
        # Central core atom (like benzene carbon ring center)
        core_atom = MolecularAtom(
            element=MolecularElement.AGGREGATE,
            name=core_name,
            x=self.center_x,
            y=self.center_y
        )
        molecule.atoms.append(core_atom)
        
        # Create hexagonal arrangement of adapter atoms
        hex_radius = 100
        for i, adapter_name in enumerate(adapters[:6]):  # Limit to 6 for perfect hexagon
            angle = (i * 60 - 90) * math.pi / 180  # Start from top (-90°)
            x = self.center_x + hex_radius * math.cos(angle)
            y = self.center_y + hex_radius * math.sin(angle)
            
            adapter_atom = MolecularAtom(
                element=MolecularElement.CONNECTOR,
                name=adapter_name,
                x=x,
                y=y
            )
            molecule.atoms.append(adapter_atom)
            
            # Create aromatic bond from core to adapter
            bond = MolecularBond(
                from_atom=core_atom,
                to_atom=adapter_atom,
                bond_type=BondType.AROMATIC
            )
            molecule.bonds.append(bond)
        
        # Connect adapters in a ring (like benzene ring)
        for i in range(len(molecule.atoms) - 1, 1, -1):
            current_adapter = molecule.atoms[i]
            next_adapter = molecule.atoms[i-1] if i > 1 else molecule.atoms[-1]
            
            ring_bond = MolecularBond(
                from_atom=current_adapter,
                to_atom=next_adapter,
                bond_type=BondType.AROMATIC
            )
            molecule.bonds.append(ring_bond)
        
        molecule.calculate_formula()
        return molecule
    
    def add_external_connections(self, molecule: HoneyprintMolecule, connections: Dict[str, str]) -> HoneyprintMolecule:
        """Add external connections like User, Database, etc."""
        for adapter_name, external_name in connections.items():
            # Find the adapter atom
            adapter_atom = None
            for atom in molecule.atoms:
                if atom.name == adapter_name:
                    adapter_atom = atom
                    break
            
            if adapter_atom:
                # Calculate position for external atom
                dx = adapter_atom.x - self.center_x
                dy = adapter_atom.y - self.center_y
                length = math.sqrt(dx*dx + dy*dy)
                unit_x, unit_y = dx/length, dy/length
                
                external_x = adapter_atom.x + unit_x * 80
                external_y = adapter_atom.y + unit_y * 80
                
                external_atom = MolecularAtom(
                    element=MolecularElement.TRANSFORMATION,
                    name=external_name,
                    x=external_x,
                    y=external_y,
                    color="#6B8E23"
                )
                molecule.atoms.append(external_atom)
                
                # Create bond to external
                external_bond = MolecularBond(
                    from_atom=adapter_atom,
                    to_atom=external_atom,
                    bond_type=BondType.SINGLE
                )
                molecule.bonds.append(external_bond)
        
        molecule.calculate_formula()
        return molecule
    
    def generate_svg(self, molecule: HoneyprintMolecule) -> str:
        """Generate beautiful SVG representation of the molecular structure"""
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg" font-family="monospace" font-size="12">
    <style>
        .core {{ fill: #fff3cd; stroke: #d4a017; stroke-width: 3; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3)); }}
        .adapter {{ fill: #f1c40f; stroke: #333; stroke-width: 2; filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.2)); }}
        .transformation {{ fill: #fff9e6; stroke: #d4a017; stroke-width: 2; }}
        .event {{ fill: #ffeb99; stroke: #d4a017; stroke-width: 2; stroke-dasharray: 3,3; }}
        .external {{ fill: #6B8E23; stroke: #333; stroke-width: 2; }}
        .bond {{ stroke: #333; stroke-width: 2; opacity: 0.7; }}
        .aromatic-bond {{ stroke: #d4a017; stroke-width: 2; opacity: 0.8; }}
        .label {{ text-anchor: middle; fill: #333; font-weight: bold; }}
        .formula {{ text-anchor: middle; fill: #d4a017; font-size: 16px; font-weight: bold; }}
        .molecule-title {{ text-anchor: middle; fill: #333; font-size: 18px; font-weight: bold; }}
    </style>
    
    <title>Honeyprint: {molecule.name}</title>
    
    <!-- Molecule title -->
    <text x="{self.width//2}" y="30" class="molecule-title">{molecule.name}</text>
    <text x="{self.width//2}" y="50" class="formula">{molecule.molecular_formula}</text>
    
    <!-- Bonds (draw first, so they appear behind atoms) -->'''
        
        for bond in molecule.bonds:
            svg_content += f"\n    {bond.get_svg_path()}"
        
        svg_content += "\n\n    <!-- Atoms -->"
        
        for atom in molecule.atoms:
            css_class = "external" if atom.color == "#6B8E23" else atom.element.name.lower()
            
            svg_content += f'''
    <circle cx="{atom.x}" cy="{atom.y}" r="{atom.radius}" class="{css_class}"/>
    <text x="{atom.x}" y="{atom.y + 5}" class="label">{atom.name}</text>'''
        
        svg_content += "\n</svg>"
        return svg_content

# Example usage and testing
def create_example_honeyprint():
    """Create an example honeyprint based on the original design"""
    generator = HoneyprintGenerator()
    
    # Create hexagonal molecule
    adapters = ["REST", "gRPC", "SQL", "Events", "Auth", "CLI"]
    molecule = generator.create_hexagonal_molecule("Core", adapters)
    
    # Add external connections
    connections = {
        "REST": "User",
        "SQL": "Database",
        "Events": "Message Bus"
    }
    molecule = generator.add_external_connections(molecule, connections)
    
    # Generate SVG
    svg_content = generator.generate_svg(molecule)
    return svg_content

if __name__ == "__main__":
    # Test the honeyprint generator
    print("🐝 Generating example honeyprint...")
    svg = create_example_honeyprint()
    print("✅ Honeyprint generated successfully!")
    print(f"📄 SVG length: {len(svg)} characters")