#!/usr/bin/env python3
"""
🧬 Polycyclic Molecular Architecture Generator
Creates sophisticated fused-ring molecular structures for complex software architectures.

Inspired by real polycyclic aromatic hydrocarbons like naphthalene, anthracene, and phenanthrene,
this generator creates chemically-authentic molecular representations of bounded contexts,
microservices, and distributed systems.
"""

import math
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum
from datetime import datetime

try:
    from honeyprint_generator import (
        MolecularElement,
        BondType,
        MolecularAtom,
        MolecularBond,
        HoneyprintMolecule,
        HoneyprintGenerator,
    )
except ImportError:
    from .honeyprint_generator import (
        MolecularElement,
        BondType,
        MolecularAtom,
        MolecularBond,
        HoneyprintMolecule,
        HoneyprintGenerator,
    )


class PolycyclicStructure(Enum):
    """Types of polycyclic aromatic hydrocarbon structures"""

    BENZENE = "benzene"  # Single hexagon (C6H6)
    NAPHTHALENE = "naphthalene"  # Fused double hexagon (C10H8)
    ANTHRACENE = "anthracene"  # Linear triple hexagon (C14H10)
    PHENANTHRENE = "phenanthrene"  # Angular triple hexagon (C14H10)
    CORONENE = "coronene"  # Super hexagon (C24H12)


class AdapterState(Enum):
    """Advanced states for adapter molecules"""

    STABLE = "stable"
    TOXIC = "toxic"  # Problematic adapter requiring attention
    SUPERPOSITION = "superposition"  # Quantum-like state with multiple behaviors
    EVOLVING = "evolving"  # Actively changing/migrating
    RESONANCE = "resonance"  # Stabilized through delocalization


@dataclass
class PolycyclicCore:
    """A core domain represented as a hexagonal ring"""

    name: str
    element: MolecularElement
    center_x: float
    center_y: float
    radius: float = 60
    color: str = "#f39c12"

    def generate_hexagon_atoms(self, atom_radius: float = 15) -> List[MolecularAtom]:
        """Generate 6 atoms forming a hexagonal ring"""
        atoms = []
        for i in range(6):
            angle = (i * 60 - 90) * math.pi / 180  # Start from top
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)

            atom = MolecularAtom(
                element=self.element,
                name=f"{self.name}_{i}",
                x=x,
                y=y,
                radius=atom_radius,
                color=self.color,
            )
            atoms.append(atom)
        return atoms


@dataclass
class PolycyclicAdapter:
    """An adapter with advanced chemical states"""

    name: str
    state: AdapterState = AdapterState.STABLE
    external_connection: Optional[str] = None
    bond_strength: float = 1.0
    evolution_target: Optional[str] = None
    toxicity_level: float = 0.0  # 0.0 = safe, 1.0 = highly toxic


class PolycyclicMoleculeGenerator(HoneyprintGenerator):
    """Advanced generator for polycyclic molecular architectures"""

    def __init__(self, width: int = 1200, height: int = 920):
        super().__init__(width, height)
        self.center_x = width // 2 - 50  # Offset for better layout
        self.center_y = height // 2 - 60

    def create_fused_dual_core(
        self,
        core_a_name: str,
        core_b_name: str,
        adapters: List[PolycyclicAdapter],
        structure_type: PolycyclicStructure = PolycyclicStructure.NAPHTHALENE,
    ) -> HoneyprintMolecule:
        """Create a fused dual-core molecule like naphthalene (A2CX pattern)"""

        molecule = HoneyprintMolecule(name=f"{core_a_name}+{core_b_name}")

        # Create two fused cores (like naphthalene)
        core_a = PolycyclicCore(
            name=core_a_name,
            element=MolecularElement.AGGREGATE,
            center_x=self.center_x - 60,
            center_y=self.center_y,
            color="#f39c12",
        )

        core_b = PolycyclicCore(
            name=core_b_name,
            element=MolecularElement.AGGREGATE,
            center_x=self.center_x + 60,
            center_y=self.center_y,
            color="#d35400",
        )

        # Generate hexagonal atoms for each core
        core_a_atoms = core_a.generate_hexagon_atoms(12)
        core_b_atoms = core_b.generate_hexagon_atoms(12)

        # Add core center atoms for labeling
        center_a = MolecularAtom(
            element=MolecularElement.AGGREGATE,
            name=core_a_name,
            x=core_a.center_x,
            y=core_a.center_y,
            radius=60,
            color="#f39c12",
        )
        center_b = MolecularAtom(
            element=MolecularElement.AGGREGATE,
            name=core_b_name,
            x=core_b.center_x,
            y=core_b.center_y,
            radius=60,
            color="#d35400",
        )

        molecule.atoms.extend([center_a, center_b])
        molecule.atoms.extend(core_a_atoms + core_b_atoms)

        # Create aromatic bonds within each hexagon
        self._create_aromatic_hexagon_bonds(molecule, core_a_atoms)
        self._create_aromatic_hexagon_bonds(molecule, core_b_atoms)

        # Create shared fused bond between cores
        shared_bond = MolecularBond(
            from_atom=center_a,
            to_atom=center_b,
            bond_type=BondType.AROMATIC,
            strength=2.0,
        )
        molecule.bonds.append(shared_bond)

        # Add adapters around the fused structure
        self._add_polycyclic_adapters(molecule, adapters, [center_a, center_b])

        molecule.calculate_formula()
        return molecule

    def create_triple_core_linear(
        self, core_names: List[str], adapters: List[PolycyclicAdapter]
    ) -> HoneyprintMolecule:
        """Create linear triple-core molecule like anthracene (A3CX pattern)"""

        molecule = HoneyprintMolecule(name="+".join(core_names))
        core_atoms = []

        # Create three linearly arranged cores
        for i, core_name in enumerate(core_names[:3]):
            core = PolycyclicCore(
                name=core_name,
                element=MolecularElement.AGGREGATE,
                center_x=self.center_x + (i - 1) * 120,
                center_y=self.center_y,
                color=["#f39c12", "#d35400", "#e67e22"][i],
            )

            center_atom = MolecularAtom(
                element=MolecularElement.AGGREGATE,
                name=core_name,
                x=core.center_x,
                y=core.center_y,
                radius=50,
                color=core.color,
            )
            core_atoms.append(center_atom)
            molecule.atoms.append(center_atom)

            # Add hexagon atoms for visual structure
            hex_atoms = core.generate_hexagon_atoms(10)
            molecule.atoms.extend(hex_atoms)
            self._create_aromatic_hexagon_bonds(molecule, hex_atoms)

        # Create linear fusion bonds
        for i in range(len(core_atoms) - 1):
            fusion_bond = MolecularBond(
                from_atom=core_atoms[i],
                to_atom=core_atoms[i + 1],
                bond_type=BondType.AROMATIC,
                strength=1.8,
            )
            molecule.bonds.append(fusion_bond)

        # Add adapters
        self._add_polycyclic_adapters(molecule, adapters, core_atoms)

        molecule.calculate_formula()
        return molecule

    def _create_aromatic_hexagon_bonds(
        self, molecule: HoneyprintMolecule, hex_atoms: List[MolecularAtom]
    ):
        """Create aromatic bonds forming a hexagonal ring"""
        for i in range(len(hex_atoms)):
            next_i = (i + 1) % len(hex_atoms)
            bond = MolecularBond(
                from_atom=hex_atoms[i],
                to_atom=hex_atoms[next_i],
                bond_type=BondType.AROMATIC,
                strength=1.0,
            )
            molecule.bonds.append(bond)

    def _add_polycyclic_adapters(
        self,
        molecule: HoneyprintMolecule,
        adapters: List[PolycyclicAdapter],
        core_atoms: List[MolecularAtom],
    ):
        """Add adapters with advanced states around polycyclic cores"""

        adapter_positions = self._calculate_adapter_positions(core_atoms, len(adapters))

        for i, (adapter, pos) in enumerate(zip(adapters, adapter_positions)):
            # Find closest core for bonding
            closest_core = min(
                core_atoms,
                key=lambda c: math.sqrt((c.x - pos[0]) ** 2 + (c.y - pos[1]) ** 2),
            )

            # Create adapter atom with state-based styling
            adapter_color = self._get_adapter_color(adapter.state)
            adapter_atom = MolecularAtom(
                element=MolecularElement.CONNECTOR,
                name=adapter.name,
                x=pos[0],
                y=pos[1],
                radius=30,
                color=adapter_color,
            )
            molecule.atoms.append(adapter_atom)

            # Create bond with appropriate strength
            bond_type = (
                BondType.DOUBLE if adapter.bond_strength > 1.5 else BondType.SINGLE
            )
            if adapter.state == AdapterState.RESONANCE:
                bond_type = BondType.AROMATIC

            adapter_bond = MolecularBond(
                from_atom=closest_core,
                to_atom=adapter_atom,
                bond_type=bond_type,
                strength=adapter.bond_strength,
            )
            molecule.bonds.append(adapter_bond)

            # Add external connection if specified
            if adapter.external_connection:
                self._add_external_connection(
                    molecule, adapter_atom, adapter.external_connection
                )

    def _calculate_adapter_positions(
        self, core_atoms: List[MolecularAtom], adapter_count: int
    ) -> List[Tuple[float, float]]:
        """Calculate optimal positions for adapters around polycyclic cores"""
        positions = []

        # Calculate bounding box of cores
        min_x = min(atom.x for atom in core_atoms) - 80
        max_x = max(atom.x for atom in core_atoms) + 80
        min_y = min(atom.y for atom in core_atoms) - 80
        max_y = max(atom.y for atom in core_atoms) + 80

        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        # Distribute adapters around the perimeter
        radius = max(max_x - center_x, max_y - center_y) + 100

        for i in range(adapter_count):
            angle = (i * 360 / adapter_count) * math.pi / 180
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            positions.append((x, y))

        return positions

    def _get_adapter_color(self, state: AdapterState) -> str:
        """Get color based on adapter state"""
        color_map = {
            AdapterState.STABLE: "#5dade2",
            AdapterState.TOXIC: "#e74c3c",
            AdapterState.SUPERPOSITION: "#9b59b6",
            AdapterState.EVOLVING: "#f39c12",
            AdapterState.RESONANCE: "#d4a017",
        }
        return color_map.get(state, "#5dade2")

    def _add_external_connection(
        self,
        molecule: HoneyprintMolecule,
        adapter_atom: MolecularAtom,
        external_name: str,
    ):
        """Add external system connection"""
        # Calculate position further out from adapter
        dx = adapter_atom.x - self.center_x
        dy = adapter_atom.y - self.center_y
        length = math.sqrt(dx * dx + dy * dy)
        unit_x, unit_y = dx / length, dy / length

        external_x = adapter_atom.x + unit_x * 60
        external_y = adapter_atom.y + unit_y * 60

        external_atom = MolecularAtom(
            element=MolecularElement.TRANSFORMATION,
            name=external_name,
            x=external_x,
            y=external_y,
            radius=22,
            color="#58d68d",
        )
        molecule.atoms.append(external_atom)

        external_bond = MolecularBond(
            from_atom=adapter_atom,
            to_atom=external_atom,
            bond_type=BondType.SINGLE,
            strength=0.8,
        )
        molecule.bonds.append(external_bond)

    def generate_advanced_svg(self, molecule: HoneyprintMolecule) -> str:
        """Generate chemically-authentic SVG with advanced features like your A2C10 example"""

        # Calculate molecular statistics
        atom_count = len(molecule.atoms)
        bond_count = len(molecule.bonds)
        stability_score = min(
            95.0,
            85
            + len(
                [a for a in molecule.atoms if a.element == MolecularElement.AGGREGATE]
            )
            * 5,
        )
        bond_energy = atom_count * 45.8 + bond_count * 12.3  # Approximate kJ/mol

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="920" xmlns="http://www.w3.org/2000/svg" font-family="'Fira Code', monospace" font-size="12" role="img" aria-label="{molecule.name} Polycyclic Molecule">
  <defs>
    <!-- Gradients -->
    <radialGradient id="coreGradientA" cx="0.5" cy="0.35">
      <stop offset="0%" style="stop-color:#fff7e6;stop-opacity:1"></stop>
      <stop offset="100%" style="stop-color:#f39c12;stop-opacity:0.9"></stop>
    </radialGradient>
    <radialGradient id="coreGradientB" cx="0.5" cy="0.35">
      <stop offset="0%" style="stop-color:#fff8f2;stop-opacity:1"></stop>
      <stop offset="100%" style="stop-color:#d35400;stop-opacity:0.9"></stop>
    </radialGradient>
    <radialGradient id="adapterGradient" cx="0.5" cy="0.3">
      <stop offset="0%" style="stop-color:#5dade2;stop-opacity:0.95"></stop>
      <stop offset="100%" style="stop-color:#2e86c1;stop-opacity:0.8"></stop>
    </radialGradient>
    <radialGradient id="externalGradient" cx="0.5" cy="0.3">
      <stop offset="0%" style="stop-color:#58d68d;stop-opacity:0.95"></stop>
      <stop offset="100%" style="stop-color:#28b463;stop-opacity:0.8"></stop>
    </radialGradient>
    <radialGradient id="toxicGradient" cx="0.5" cy="0.3">
      <stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:0.95"></stop>
      <stop offset="100%" style="stop-color:#e74c3c;stop-opacity:0.8"></stop>
    </radialGradient>
    <linearGradient id="bgGradient" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#f4fbf9"></stop>
      <stop offset="100%" stop-color="#f6f9ff"></stop>
    </linearGradient>
    <linearGradient id="stabilityGradient" x1="0" x2="1">
      <stop offset="0%" stop-color="#58d68d" />
      <stop offset="100%" stop-color="#d35400" />
    </linearGradient>

    <!-- Filters -->
    <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="3" dy="3" stdDeviation="4" flood-color="rgba(0,0,0,0.28)"></feDropShadow>
    </filter>
    <filter id="toxicGlow">
      <feGaussianBlur stdDeviation="3" result="blur"></feGaussianBlur>
      <feComposite in="SourceGraphic" in2="blur" operator="over"></feComposite>
    </filter>
    <filter id="pulse">
      <feGaussianBlur in="SourceGraphic" stdDeviation="2" result="blur"></feGaussianBlur>
      <feComposite in="SourceGraphic" in2="blur" operator="over"></feComposite>
    </filter>
    <filter id="resonanceGlow">
      <feGaussianBlur stdDeviation="2" result="blur"></feGaussianBlur>
      <feComposite in="SourceGraphic" in2="blur" operator="over"></feComposite>
    </filter>

    <!-- Styles -->
    <style>
      .background {{ fill: url(#bgGradient); }}
      .coreA {{ fill: url(#coreGradientA); stroke:#c07210; stroke-width:3; filter: url(#shadow); }}
      .coreB {{ fill: url(#coreGradientB); stroke:#b24a0d; stroke-width:3; filter: url(#shadow); }}
      .adapter {{ fill: url(#adapterGradient); stroke:#1f4e79; stroke-width:2; filter: url(#shadow); }}
      .toxic {{ fill: url(#toxicGradient); stroke:#c0392b; stroke-width:2; filter: url(#toxicGlow); }}
      .external {{ fill: url(#externalGradient); stroke:#1e8449; stroke-width:2; filter: url(#shadow); }}
      .bond {{ stroke: #34495e; stroke-width:2; stroke-linecap: round; opacity:0.9; }}
      .strong-bond {{ stroke: #34495e; stroke-width:4; stroke-linecap: round; opacity:0.9; }}
      .weak-bond {{ stroke: #34495e; stroke-width:1; stroke-linecap: round; opacity:0.6; stroke-dasharray: 3,2; }}
      .aromatic {{ stroke: #d4a017; stroke-width:2; stroke-dasharray: 8,4; opacity:0.95; stroke-linecap: round; }}
      .resonance {{ stroke: #d4a017; stroke-width:2; stroke-dasharray: 5,3; opacity:0.7; stroke-linecap: round; }}
      .label {{ text-anchor: middle; fill: #2c3e50; font-weight: bold; font-size:12px; }}
      .core-label {{ text-anchor: middle; fill: #6b2f00; font-weight: bold; font-size:13px; }}
      .title {{ text-anchor: middle; fill: #2c3e50; font-size:22px; font-weight:bold; }}
      .formula {{ text-anchor: middle; fill: #d4a017; font-size:18px; font-weight:bold; }}
      .stats {{ fill: #34495e; font-size:12px; }}
      .small {{ font-size:11px; fill:#2c3e50; }}
      .legend {{ fill: rgba(255,255,255,0.95); stroke:#bdc3c7; stroke-width:1; }}
      .toxic-label {{ fill: #e74c3c; font-size:10px; font-weight:bold; }}
      .evolution {{ stroke: #d4a017; stroke-width:1; stroke-dasharray: 5,3; opacity:0.7; }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="1200" height="920" class="background"></rect>

  <!-- Title -->
  <text x="600" y="38" class="title">🧪 {molecule.name} — Polycyclic Molecule ({molecule.molecular_formula})</text>
  <text x="600" y="64" class="formula">{molecule.molecular_formula}</text>'''

        # Add aromatic bonds first (background layer)
        svg_content += "\n\n  <!-- Aromatic Ring Structures -->"
        core_atoms = [
            a for a in molecule.atoms if a.element == MolecularElement.AGGREGATE
        ]

        for core in core_atoms[:2]:  # Draw hexagons around first two cores
            hex_x, hex_y = core.x, core.y
            hex_radius = 60
            svg_content += f'''
  <g transform="translate({hex_x},{hex_y})">
    <line x1="0" y1="-{hex_radius * 2}" x2="{hex_radius * 1.73 / 2}" y2="-{hex_radius}" class="aromatic"></line>
    <line x1="{hex_radius * 1.73 / 2}" y1="-{hex_radius}" x2="{hex_radius * 1.73 / 2}" y2="{hex_radius}" class="aromatic"></line>
    <line x1="{hex_radius * 1.73 / 2}" y1="{hex_radius}" x2="0" y2="{hex_radius * 2}" class="aromatic"></line>
    <line x1="0" y1="{hex_radius * 2}" x2="-{hex_radius * 1.73 / 2}" y2="{hex_radius}" class="aromatic"></line>
    <line x1="-{hex_radius * 1.73 / 2}" y1="{hex_radius}" x2="-{hex_radius * 1.73 / 2}" y2="-{hex_radius}" class="aromatic"></line>
    <line x1="-{hex_radius * 1.73 / 2}" y1="-{hex_radius}" x2="0" y2="-{hex_radius * 2}" class="aromatic"></line>
  </g>'''

        # Add molecular bonds
        svg_content += "\n\n  <!-- Molecular Bonds -->"
        for bond in molecule.bonds:
            bond_class = (
                "aromatic"
                if bond.bond_type == BondType.AROMATIC
                else "strong-bond"
                if bond.strength > 1.5
                else "weak-bond"
                if bond.strength < 1.0
                else "bond"
            )

            # Add animation for strong bonds
            animation = ""
            if bond.strength > 1.5:
                animation = """
      <animate attributeName="stroke-width" values="2;4;2" dur="2s" repeatCount="indefinite"></animate>"""

            svg_content += f'''
  <line x1="{bond.from_atom.x}" y1="{bond.from_atom.y}" x2="{bond.to_atom.x}" y2="{bond.to_atom.y}" class="{bond_class}">{animation}
  </line>'''

        # Add atoms
        svg_content += "\n\n  <!-- Molecular Atoms -->"
        for atom in molecule.atoms:
            if atom.element == MolecularElement.AGGREGATE:
                css_class = "coreA" if atom.color == "#f39c12" else "coreB"
            elif atom.color == "#e74c3c":
                css_class = "toxic"
            elif atom.element == MolecularElement.TRANSFORMATION:
                css_class = "external"
            else:
                css_class = "adapter"

            # Add special effects for some atoms
            filter_attr = ""
            if css_class == "toxic":
                filter_attr = ' style="filter: url(#toxicGlow)"'
            elif atom.name in ["Gateway", "Audit"]:
                filter_attr = ' style="filter: url(#resonanceGlow)"'
            elif atom.name in ["AuthZ", "GraphQL"]:
                filter_attr = ' style="filter: url(#pulse)"'

            svg_content += f'''
  <g>
    <circle cx="{atom.x}" cy="{atom.y}" r="{atom.radius}" class="{css_class}"{filter_attr}></circle>
    <text x="{atom.x}" y="{atom.y - 6}" class="{"core-label" if atom.element == MolecularElement.AGGREGATE else "label"}">{atom.name.split("_")[0]}</text>'''

            if atom.element == MolecularElement.AGGREGATE:
                svg_content += f'''
    <text x="{atom.x}" y="{atom.y + 14}" class="core-label">Core</text>'''
            elif atom.name == "REST":
                svg_content += f'''
    <text x="{atom.x}" y="{atom.y + 17}" class="toxic-label">(Toxic)</text>'''
            elif atom.name == "AuthZ":
                svg_content += f'''
    <text x="{atom.x}" y="{atom.y + 17}" class="small">(Superposition)</text>'''
            elif atom.name == "Cache":
                svg_content += f'''
    <text x="{atom.x}" y="{atom.y + 17}" class="small">(Pollinated)</text>'''

            svg_content += "\n  </g>"

        # Add molecular statistics
        svg_content += f"""

  <!-- Molecular Statistics -->
  <rect x="20" y="560" width="260" height="130" class="legend" rx="10"></rect>
  <text x="40" y="585" class="stats" font-weight="bold">🔬 Molecular Analysis</text>
  <text x="40" y="605" class="stats">Formula: {molecule.molecular_formula}</text>
  <text x="40" y="620" class="stats">Stability: {stability_score:.1f} / 100 (Polycyclic aromatic)</text>
  <text x="40" y="635" class="stats">Bond Energy: {bond_energy:.0f} kJ/mol</text>
  <text x="40" y="650" class="stats">Atoms: {atom_count} | Bonds: {bond_count}</text>

  <rect x="620" y="560" width="260" height="130" class="legend" rx="10"></rect>
  <text x="640" y="585" class="stats" font-weight="bold">⚗️ Synthesis Details</text>
  <text x="640" y="605" class="stats">Catalyst: Royal Jelly + Policy Council</text>
  <text x="640" y="620" class="stats">Temperature: 310K</text>
  <text x="640" y="635" class="stats">Pattern: Fused Hexagonal Core (Naphthalene-like)</text>
  <text x="640" y="650" class="stats">Generated: {current_time}</text>

  <!-- Stability Heatmap -->
  <rect x="500" y="50" width="100" height="20" fill="url(#stabilityGradient)"></rect>
  <text x="550" y="65" class="small" text-anchor="middle">Stability: {stability_score:.0f}%</text>

  <!-- Legend -->
  <rect x="20" y="90" width="220" height="160" rx="8" class="legend"></rect>
  <text x="40" y="110" class="stats" font-weight="bold">🧪 Legend</text>
  <circle cx="40" cy="130" r="8" class="coreA"></circle>
  <text x="60" y="135" class="small">Aromatic Core (Domain)</text>
  <circle cx="40" cy="150" r="8" class="adapter"></circle>
  <text x="60" y="155" class="small">Adapters (Connectors)</text>
  <circle cx="40" cy="170" r="8" class="toxic"></circle>
  <text x="60" y="175" class="small">Toxic Adapters</text>
  <circle cx="40" cy="190" r="8" class="external"></circle>
  <text x="60" y="195" class="small">External Systems</text>
  <line x1="30" y1="210" x2="70" y2="210" class="aromatic"></line>
  <text x="80" y="215" class="small">Aromatic bond (stability)</text>
  <line x1="30" y1="230" x2="70" y2="230" class="strong-bond"></line>
  <text x="80" y="235" class="small">Strong bond (high traffic)</text>
  <line x1="30" y1="250" x2="70" y2="250" class="weak-bond"></line>
  <text x="80" y="255" class="small">Weak bond (low traffic)</text>

  <!-- Footer -->
  <text x="600" y="880" class="small" text-anchor="middle">
    🧬 Polycyclic Architecture: Fused bounded contexts with shared molecular orbitals and aromatic stability.
    Generated by Genesis Engine Molecular Architecture System.
  </text>
</svg>"""

        return svg_content


def create_identity_access_molecule() -> str:
    """Create the A2C10 Identity+Access molecule like the example"""

    generator = PolycyclicMoleculeGenerator()

    # Define adapters with advanced states
    adapters = [
        PolycyclicAdapter(
            "REST", AdapterState.TOXIC, "Mobile", 1.5, toxicity_level=0.8
        ),
        PolycyclicAdapter(
            "GraphQL", AdapterState.EVOLVING, "Web", 1.2, evolution_target="GraphQL_v2"
        ),
        PolycyclicAdapter("Gateway", AdapterState.RESONANCE, "API_GW", 1.0),
        PolycyclicAdapter("DB", AdapterState.STABLE, "Postgres", 1.8),
        PolycyclicAdapter("EventBus", AdapterState.STABLE, "MessageQueue", 1.0),
        PolycyclicAdapter("Metrics", AdapterState.STABLE, "Prometheus", 0.9),
        PolycyclicAdapter("AuthZ", AdapterState.SUPERPOSITION, "Policy", 1.3),
        PolycyclicAdapter("Cache", AdapterState.STABLE, "Redis", 1.1),
        PolycyclicAdapter("Audit", AdapterState.RESONANCE, "SIEM", 1.6),
    ]

    # Create fused Identity+Access cores
    molecule = generator.create_fused_dual_core("Identity", "Access", adapters)

    # Generate advanced SVG with chemical authenticity
    svg_content = generator.generate_advanced_svg(molecule)

    return svg_content


if __name__ == "__main__":
    print("🧬 Generating A2C10 Identity+Access polycyclic molecule...")
    svg = create_identity_access_molecule()

    with open("A2C10_Identity_Access.svg", "w") as f:
        f.write(svg)

    print("✅ A2C10 molecule generated successfully!")
    print(f"📄 SVG length: {len(svg)} characters")
