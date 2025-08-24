#!/usr/bin/env python3
"""
🧬 Advanced Molecular Architecture Templates
Next-generation molecular templates inspired by sophisticated chemical structures:

- Fullerenes (C60, C70): For containerized and microservice architectures
- Carbon Nanotubes: For pipeline and streaming architectures
- Protein Structures: For complex service interactions (α-helices, β-sheets)
- DNA Double Helix: For replication and inheritance patterns
- Crystal Lattices: For grid and distributed system architectures
- Cyclodextrins: For host-guest architectural patterns
"""

import math
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum

try:
    from .advanced_molecular_visualizer import (
        AdvancedMolecularAtom,
        AdvancedMolecularBond,
        AdvancedMolecularVisualizer,
        QuantumState,
        ThermodynamicPhase,
        AdvancedBondType,
        MolecularOrbitalType,
        QuantumProperties,
        ThermodynamicProperties,
    )
    from .honeyprint_generator import MolecularElement, HoneyprintMolecule
except ImportError:
    from advanced_molecular_visualizer import (
        AdvancedMolecularAtom,
        AdvancedMolecularBond,
        AdvancedMolecularVisualizer,
        QuantumState,
        ThermodynamicPhase,
        AdvancedBondType,
    )
    from honeyprint_generator import MolecularElement, HoneyprintMolecule


class AdvancedStructureType(Enum):
    """Advanced molecular structure types for complex architectures"""

    FULLERENE_C60 = "fullerene_c60"  # Soccer ball structure for containers
    FULLERENE_C70 = "fullerene_c70"  # Rugby ball for elongated services
    CARBON_NANOTUBE = "carbon_nanotube"  # Cylinder for data pipelines
    ALPHA_HELIX = "alpha_helix"  # Spiral for sequential processing
    BETA_SHEET = "beta_sheet"  # Parallel/antiparallel service layers
    DNA_DOUBLE_HELIX = "dna_double_helix"  # Replication and version control
    FACE_CENTERED_CUBIC = "fcc_crystal"  # Grid compute architectures
    BODY_CENTERED_CUBIC = "bcc_crystal"  # Distributed storage systems
    CYCLODEXTRIN = "cyclodextrin"  # Host-guest service patterns
    GRAPHENE_SHEET = "graphene_sheet"  # 2D distributed systems
    DIAMOND_LATTICE = "diamond_lattice"  # Ultra-stable architectures


class ProteinSecondaryStructure(Enum):
    """Protein secondary structure types"""

    ALPHA_HELIX = "alpha_helix"
    BETA_SHEET = "beta_sheet"
    BETA_TURN = "beta_turn"
    RANDOM_COIL = "random_coil"


@dataclass
class StructuralParameters:
    """Parameters for advanced molecular structures"""

    radius: float = 100.0  # Base radius for structure
    height: float = 200.0  # Height for cylindrical structures
    twist_angle: float = 36.0  # Degrees per turn for helices
    layer_spacing: float = 3.4  # Angstroms between layers
    bond_angle: float = 109.5  # Tetrahedral angle in degrees

    # Container-specific parameters
    wall_thickness: float = 5.0  # For fullerenes and nanotubes
    opening_size: float = 15.0  # For host-guest structures

    # Crystal parameters
    lattice_constant: float = 4.0  # Angstroms for crystal spacing
    unit_cells: Tuple[int, int, int] = (3, 3, 3)  # Number of unit cells


class AdvancedMolecularTemplates:
    """Generator for advanced molecular architecture templates"""

    def __init__(self, visualizer: AdvancedMolecularVisualizer = None):
        self.visualizer = visualizer or AdvancedMolecularVisualizer()

    def create_fullerene_c60(
        self, center_x: float, center_y: float, params: StructuralParameters = None
    ) -> Tuple[List[AdvancedMolecularAtom], List[AdvancedMolecularBond]]:
        """Create a C60 fullerene (buckminsterfullerene) structure for container architectures"""

        if params is None:
            params = StructuralParameters()

        atoms = []
        bonds = []

        # C60 has 60 carbon atoms arranged in a soccer ball pattern
        # Simplified representation with pentagons and hexagons

        # Create the characteristic pentagon-hexagon pattern
        # 12 pentagons and 20 hexagons

        # Generate atoms on a geodesic sphere
        for i in range(60):
            # Use golden ratio for uniform distribution on sphere
            phi = math.acos(1 - 2 * (i + 0.5) / 60)
            theta = math.pi * (1 + 5**0.5) * i

            x = center_x + params.radius * math.sin(phi) * math.cos(theta)
            y = center_y + params.radius * math.sin(phi) * math.sin(theta)

            atom = AdvancedMolecularAtom(
                element=MolecularElement.CONNECTOR,
                name=f"C{i + 1}",
                x=x,
                y=y,
                radius=8,
                color="#2c3e50",
            )

            # Fullerenes exhibit special quantum properties
            atom.quantum_props.state = QuantumState.COHERENT
            atom.quantum_props.energy_level = 2.5
            atom.thermo_props.phase = ThermodynamicPhase.SOLID
            atom.hybridization = "sp2"

            atoms.append(atom)

        # Create bonds between nearest neighbors (simplified pattern)
        for i, atom in enumerate(atoms):
            # Connect to next 3 atoms in cyclic pattern (simplified)
            for j in range(1, 4):
                next_idx = (i + j) % len(atoms)
                if next_idx > i:  # Avoid duplicate bonds
                    bond = AdvancedMolecularBond(
                        from_atom=atom,
                        to_atom=atoms[next_idx],
                        advanced_type=AdvancedBondType.COVALENT,
                        bond_order=1.5,  # Aromatic character
                        bond_energy=518.0,
                    )
                    bonds.append(bond)

        return atoms, bonds

    def create_carbon_nanotube(
        self, start_x: float, start_y: float, params: StructuralParameters = None
    ) -> Tuple[List[AdvancedMolecularAtom], List[AdvancedMolecularBond]]:
        """Create a carbon nanotube structure for pipeline architectures"""

        if params is None:
            params = StructuralParameters(radius=40, height=300)

        atoms = []
        bonds = []

        # Single-walled carbon nanotube (SWCNT)
        # Zigzag or armchair pattern

        circumference = 2 * math.pi * params.radius
        atoms_per_ring = int(circumference / 2.5)  # Approximate carbon spacing
        num_rings = int(params.height / params.layer_spacing)

        for ring in range(num_rings):
            y = start_y + ring * params.layer_spacing

            for i in range(atoms_per_ring):
                angle = 2 * math.pi * i / atoms_per_ring
                x = start_x + params.radius * math.cos(angle)

                atom = AdvancedMolecularAtom(
                    element=MolecularElement.CONNECTOR,
                    name=f"C{ring}_{i}",
                    x=x,
                    y=y,
                    radius=6,
                    color="#34495e",
                )

                # Nanotubes have unique electronic properties
                atom.quantum_props.state = QuantumState.COHERENT
                atom.quantum_props.energy_level = 1.8
                atom.thermo_props.phase = ThermodynamicPhase.SOLID
                atom.hybridization = "sp2"

                atoms.append(atom)

                # Create bonds within ring
                if i > 0:
                    prev_atom = atoms[-2]
                    bond = AdvancedMolecularBond(
                        from_atom=prev_atom,
                        to_atom=atom,
                        advanced_type=AdvancedBondType.COVALENT,
                        bond_order=1.5,
                        bond_energy=518.0,
                    )
                    bonds.append(bond)

                # Close the ring
                if i == atoms_per_ring - 1:
                    first_in_ring = atoms[-atoms_per_ring]
                    bond = AdvancedMolecularBond(
                        from_atom=atom,
                        to_atom=first_in_ring,
                        advanced_type=AdvancedBondType.COVALENT,
                        bond_order=1.5,
                        bond_energy=518.0,
                    )
                    bonds.append(bond)

                # Create bonds between rings
                if ring > 0:
                    prev_ring_atom = atoms[-(atoms_per_ring + i + 1)]
                    bond = AdvancedMolecularBond(
                        from_atom=prev_ring_atom,
                        to_atom=atom,
                        advanced_type=AdvancedBondType.COVALENT,
                        bond_order=1.5,
                        bond_energy=518.0,
                    )
                    bonds.append(bond)

        return atoms, bonds

    def create_alpha_helix(
        self, center_x: float, center_y: float, params: StructuralParameters = None
    ) -> Tuple[List[AdvancedMolecularAtom], List[AdvancedMolecularBond]]:
        """Create an α-helix structure for sequential processing architectures"""

        if params is None:
            params = StructuralParameters(radius=25, height=200, twist_angle=100)

        atoms = []
        bonds = []

        # Alpha helix: right-handed helix with 3.6 residues per turn
        residues_per_turn = 3.6
        rise_per_residue = 1.5  # Angstroms
        num_residues = int(params.height / rise_per_residue)

        for i in range(num_residues):
            # Calculate helical coordinates
            t = i / residues_per_turn  # Turns
            angle = 2 * math.pi * t
            z = i * rise_per_residue

            x = center_x + params.radius * math.cos(angle)
            y = center_y + z  # Using y as height in 2D projection

            # Alternate between different service types
            if i % 4 == 0:
                element = MolecularElement.AGGREGATE
                color = "#e74c3c"
                name = f"Service{i // 4 + 1}"
            elif i % 4 == 1:
                element = MolecularElement.TRANSFORMATION
                color = "#f39c12"
                name = f"Transform{i // 4 + 1}"
            elif i % 4 == 2:
                element = MolecularElement.CONNECTOR
                color = "#3498db"
                name = f"Connect{i // 4 + 1}"
            else:
                element = MolecularElement.GENESIS_EVENT
                color = "#9b59b6"
                name = f"Event{i // 4 + 1}"

            atom = AdvancedMolecularAtom(
                element=element, name=name, x=x, y=y, radius=15, color=color
            )

            # Helical structures have regular patterns
            atom.quantum_props.state = QuantumState.COHERENT
            atom.quantum_props.energy_level = 1.2
            atom.thermo_props.phase = ThermodynamicPhase.LIQUID  # Flexible

            atoms.append(atom)

            # Create backbone bonds (peptide bonds)
            if i > 0:
                bond = AdvancedMolecularBond(
                    from_atom=atoms[-2],
                    to_atom=atom,
                    advanced_type=AdvancedBondType.COVALENT,
                    bond_order=1.0,
                    bond_energy=350.0,
                )
                bonds.append(bond)

            # Create hydrogen bonds (helix stabilization)
            if i >= 4:  # i-4 residue hydrogen bonding
                h_bond = AdvancedMolecularBond(
                    from_atom=atoms[i - 4],
                    to_atom=atom,
                    advanced_type=AdvancedBondType.HYDROGEN,
                    bond_order=0.3,
                    bond_energy=20.0,
                )
                bonds.append(h_bond)

        return atoms, bonds

    def create_beta_sheet(
        self,
        start_x: float,
        start_y: float,
        params: StructuralParameters = None,
        parallel: bool = True,
    ) -> Tuple[List[AdvancedMolecularAtom], List[AdvancedMolecularBond]]:
        """Create a β-sheet structure for layered service architectures"""

        if params is None:
            params = StructuralParameters(layer_spacing=10, height=150)

        atoms = []
        bonds = []

        num_strands = 4
        residues_per_strand = 8

        for strand in range(num_strands):
            y_offset = start_y + strand * params.layer_spacing * 3

            strand_atoms = []

            for res in range(residues_per_strand):
                # Zigzag pattern for beta sheet
                x_offset = (
                    res * 7 if strand % 2 == 0 else (residues_per_strand - res - 1) * 7
                )
                x = start_x + x_offset
                y = y_offset + (res % 2) * 3  # Slight zigzag

                # Service layer types
                if strand == 0:
                    element = MolecularElement.AGGREGATE
                    color = "#e74c3c"
                    name = f"Controller{res + 1}"
                elif strand == 1:
                    element = MolecularElement.TRANSFORMATION
                    color = "#f39c12"
                    name = f"Business{res + 1}"
                elif strand == 2:
                    element = MolecularElement.CONNECTOR
                    color = "#3498db"
                    name = f"Data{res + 1}"
                else:
                    element = MolecularElement.GENESIS_EVENT
                    color = "#9b59b6"
                    name = f"Event{res + 1}"

                atom = AdvancedMolecularAtom(
                    element=element, name=name, x=x, y=y, radius=12, color=color
                )

                atom.quantum_props.state = QuantumState.GROUND
                atom.thermo_props.phase = ThermodynamicPhase.SOLID  # Stable layers

                atoms.append(atom)
                strand_atoms.append(atom)

                # Backbone bonds within strand
                if res > 0:
                    bond = AdvancedMolecularBond(
                        from_atom=strand_atoms[-2],
                        to_atom=atom,
                        advanced_type=AdvancedBondType.COVALENT,
                        bond_order=1.0,
                        bond_energy=350.0,
                    )
                    bonds.append(bond)

            # Inter-strand hydrogen bonds
            if strand > 0:
                prev_strand_start = len(atoms) - 2 * residues_per_strand
                for res in range(residues_per_strand):
                    current_atom = atoms[prev_strand_start + residues_per_strand + res]

                    # Hydrogen bond pattern depends on parallel vs antiparallel
                    if parallel:
                        target_res = res
                    else:
                        target_res = residues_per_strand - res - 1

                    if target_res < residues_per_strand:
                        prev_atom = atoms[prev_strand_start + target_res]
                        h_bond = AdvancedMolecularBond(
                            from_atom=prev_atom,
                            to_atom=current_atom,
                            advanced_type=AdvancedBondType.HYDROGEN,
                            bond_order=0.3,
                            bond_energy=18.0,
                        )
                        bonds.append(h_bond)

        return atoms, bonds

    def create_dna_double_helix(
        self, center_x: float, center_y: float, params: StructuralParameters = None
    ) -> Tuple[List[AdvancedMolecularAtom], List[AdvancedMolecularBond]]:
        """Create a DNA double helix for replication and inheritance patterns"""

        if params is None:
            params = StructuralParameters(radius=15, height=300, twist_angle=36)

        atoms = []
        bonds = []

        base_pairs = ["AT", "GC", "TA", "CG"] * 10  # 40 base pairs
        rise_per_bp = 3.4  # Angstroms

        for i, bp in enumerate(base_pairs):
            angle = i * params.twist_angle * math.pi / 180
            y = center_y + i * rise_per_bp

            # First strand (left)
            x1 = center_x - params.radius * math.cos(angle)
            base1 = bp[0]

            atom1 = AdvancedMolecularAtom(
                element=MolecularElement.AGGREGATE
                if base1 in "AT"
                else MolecularElement.CONNECTOR,
                name=f"{base1}{i + 1}",
                x=x1,
                y=y,
                radius=10,
                color="#e74c3c" if base1 in "AT" else "#3498db",
            )

            # Second strand (right)
            x2 = center_x + params.radius * math.cos(angle)
            base2 = bp[1]

            atom2 = AdvancedMolecularAtom(
                element=MolecularElement.TRANSFORMATION
                if base2 in "AT"
                else MolecularElement.GENESIS_EVENT,
                name=f"{base2}{i + 1}",
                x=x2,
                y=y,
                radius=10,
                color="#f39c12" if base2 in "AT" else "#9b59b6",
            )

            # DNA exhibits quantum coherence in some theories
            atom1.quantum_props.state = QuantumState.COHERENT
            atom2.quantum_props.state = QuantumState.COHERENT
            atom1.quantum_props.energy_level = 0.8
            atom2.quantum_props.energy_level = 0.8

            atoms.extend([atom1, atom2])

            # Hydrogen bonds between base pairs
            if base1 == "A" and base2 == "T":
                bond_energy = 8.0  # 2 H-bonds
            elif base1 == "G" and base2 == "C":
                bond_energy = 12.0  # 3 H-bonds
            elif base1 == "T" and base2 == "A":
                bond_energy = 8.0
            else:  # G-C
                bond_energy = 12.0

            bp_bond = AdvancedMolecularBond(
                from_atom=atom1,
                to_atom=atom2,
                advanced_type=AdvancedBondType.HYDROGEN,
                bond_order=0.4,
                bond_energy=bond_energy,
            )
            bonds.append(bp_bond)

            # Backbone bonds (sugar-phosphate)
            if i > 0:
                # Connect to previous base in same strand
                backbone1 = AdvancedMolecularBond(
                    from_atom=atoms[-4],  # Previous atom1
                    to_atom=atom1,
                    advanced_type=AdvancedBondType.COVALENT,
                    bond_order=1.0,
                    bond_energy=420.0,
                )
                bonds.append(backbone1)

                backbone2 = AdvancedMolecularBond(
                    from_atom=atoms[-3],  # Previous atom2
                    to_atom=atom2,
                    advanced_type=AdvancedBondType.COVALENT,
                    bond_order=1.0,
                    bond_energy=420.0,
                )
                bonds.append(backbone2)

        return atoms, bonds

    def create_crystal_lattice(
        self,
        center_x: float,
        center_y: float,
        structure_type: AdvancedStructureType,
        params: StructuralParameters = None,
    ) -> Tuple[List[AdvancedMolecularAtom], List[AdvancedMolecularBond]]:
        """Create crystal lattice structures for distributed system architectures"""

        if params is None:
            params = StructuralParameters(lattice_constant=30)

        atoms = []
        bonds = []

        if structure_type == AdvancedStructureType.FACE_CENTERED_CUBIC:
            # FCC: atoms at corners and face centers
            positions = [
                (0, 0),
                (1, 0),
                (0, 1),
                (1, 1),  # Corners (2D projection)
                (0.5, 0.5),  # Face center
            ]

            for i in range(params.unit_cells[0]):
                for j in range(params.unit_cells[1]):
                    for pos in positions:
                        x = center_x + (i + pos[0]) * params.lattice_constant
                        y = center_y + (j + pos[1]) * params.lattice_constant

                        atom = AdvancedMolecularAtom(
                            element=MolecularElement.CONNECTOR,
                            name=f"Node{len(atoms) + 1}",
                            x=x,
                            y=y,
                            radius=8,
                            color="#2ecc71",
                        )

                        atom.thermo_props.phase = ThermodynamicPhase.SOLID
                        atoms.append(atom)

        elif structure_type == AdvancedStructureType.BODY_CENTERED_CUBIC:
            # BCC: atoms at corners and body center
            positions = [
                (0, 0),
                (1, 0),
                (0, 1),
                (1, 1),  # Corners
                (0.5, 0.5),  # Body center
            ]

            for i in range(params.unit_cells[0]):
                for j in range(params.unit_cells[1]):
                    for pos in positions:
                        x = center_x + (i + pos[0]) * params.lattice_constant
                        y = center_y + (j + pos[1]) * params.lattice_constant

                        atom = AdvancedMolecularAtom(
                            element=MolecularElement.AGGREGATE,
                            name=f"Core{len(atoms) + 1}",
                            x=x,
                            y=y,
                            radius=10,
                            color="#e67e22",
                        )

                        atom.thermo_props.phase = ThermodynamicPhase.SOLID
                        atoms.append(atom)

        # Create nearest neighbor bonds
        for i, atom1 in enumerate(atoms):
            for j, atom2 in enumerate(atoms[i + 1 :], i + 1):
                distance = math.sqrt(
                    (atom1.x - atom2.x) ** 2 + (atom1.y - atom2.y) ** 2
                )

                # Bond if within nearest neighbor distance
                if distance <= params.lattice_constant * 1.1:
                    bond = AdvancedMolecularBond(
                        from_atom=atom1,
                        to_atom=atom2,
                        advanced_type=AdvancedBondType.METALLIC,
                        bond_order=0.5,  # Delocalized bonding
                        bond_energy=200.0,
                    )
                    bonds.append(bond)

        return atoms, bonds

    def create_template_molecule(
        self,
        structure_type: AdvancedStructureType,
        name: str,
        center_x: float = 500,
        center_y: float = 400,
        params: StructuralParameters = None,
    ) -> HoneyprintMolecule:
        """Create a complete molecule from an advanced template"""

        atoms, bonds = [], []

        if structure_type == AdvancedStructureType.FULLERENE_C60:
            atoms, bonds = self.create_fullerene_c60(center_x, center_y, params)
        elif structure_type == AdvancedStructureType.CARBON_NANOTUBE:
            atoms, bonds = self.create_carbon_nanotube(center_x, center_y, params)
        elif structure_type == AdvancedStructureType.ALPHA_HELIX:
            atoms, bonds = self.create_alpha_helix(center_x, center_y, params)
        elif structure_type == AdvancedStructureType.BETA_SHEET:
            atoms, bonds = self.create_beta_sheet(center_x, center_y, params)
        elif structure_type == AdvancedStructureType.DNA_DOUBLE_HELIX:
            atoms, bonds = self.create_dna_double_helix(center_x, center_y, params)
        elif structure_type in [
            AdvancedStructureType.FACE_CENTERED_CUBIC,
            AdvancedStructureType.BODY_CENTERED_CUBIC,
        ]:
            atoms, bonds = self.create_crystal_lattice(
                center_x, center_y, structure_type, params
            )

        molecule = self.visualizer.create_quantum_enhanced_molecule(name, atoms, bonds)
        return molecule


def create_advanced_template_examples():
    """Create examples of all advanced molecular templates"""
    templates = AdvancedMolecularTemplates()

    examples = {
        "fullerene_container": templates.create_template_molecule(
            AdvancedStructureType.FULLERENE_C60, "ContainerArchitecture_C60", 400, 300
        ),
        "nanotube_pipeline": templates.create_template_molecule(
            AdvancedStructureType.CARBON_NANOTUBE,
            "DataPipeline_CNT",
            600,
            200,
            StructuralParameters(radius=25, height=200),
        ),
        "helix_sequence": templates.create_template_molecule(
            AdvancedStructureType.ALPHA_HELIX,
            "SequentialProcessing_αHelix",
            300,
            400,
            StructuralParameters(radius=30, height=250),
        ),
        "sheet_layers": templates.create_template_molecule(
            AdvancedStructureType.BETA_SHEET,
            "LayeredServices_βSheet",
            500,
            500,
            StructuralParameters(layer_spacing=15),
        ),
        "dna_replication": templates.create_template_molecule(
            AdvancedStructureType.DNA_DOUBLE_HELIX,
            "ReplicationSystem_DNA",
            700,
            300,
            StructuralParameters(radius=20, height=300),
        ),
    }

    return examples


if __name__ == "__main__":
    print("🧬 Generating advanced molecular templates...")

    templates = AdvancedMolecularTemplates()
    visualizer = AdvancedMolecularVisualizer()

    # Create a fullerene example
    fullerene = templates.create_template_molecule(
        AdvancedStructureType.FULLERENE_C60, "MicroserviceContainer_C60"
    )

    svg_content = visualizer.generate_enhanced_svg(fullerene)

    with open("fullerene_c60_template.svg", "w") as f:
        f.write(svg_content)

    print("✅ Advanced molecular templates generated successfully!")
    print(f"📄 Fullerene C60 SVG length: {len(svg_content)} characters")
