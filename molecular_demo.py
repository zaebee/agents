#!/usr/bin/env python3
"""
🧪 Molecular Architecture Demonstration
Shows the complete molecular synthesis and visualization system.
"""

import asyncio
import sys
from pathlib import Path

# Add genesis-engine to path
sys.path.insert(0, str(Path(__file__).parent / "genesis-engine"))

# Import our molecular components
from transformations.honeyprint_generator import (
    HoneyprintGenerator,
    create_example_honeyprint,
)
from transformations.reaction_engine import ReactionEngine
from aggregates.molecular_analyzer import MolecularAnalyzer
from connectors.chemical_registry import (
    ChemicalRegistry,
)
from aggregates.queen_bee import QueenBee

from datetime import datetime


def print_banner(text, emoji="🧪"):
    """Print a beautiful banner"""
    print(f"\n{emoji} {text}")
    print("=" * (len(text) + 4))


def print_result(label, value, unit=""):
    """Print a formatted result"""
    print(f"   {label}: {value}{unit}")


async def molecular_growth_demo():
    """Complete demonstration of molecular growth and visualization"""

    print_banner("MOLECULAR ARCHITECTURE DEMONSTRATION", "🧬")
    print("Growing software molecules using chemistry principles!")

    # Step 1: Initialize the molecular system
    print_banner("Phase 1: System Initialization", "⚡")

    print("🔬 Initializing molecular chemistry components...")
    honeyprint_gen = HoneyprintGenerator()
    reaction_engine = ReactionEngine()
    molecular_analyzer = MolecularAnalyzer()
    chemical_registry = ChemicalRegistry()
    queen_bee = QueenBee()

    print("✅ All molecular systems online!")

    # Step 2: Show available blueprints
    print_banner("Phase 2: Architectural Blueprints", "📋")

    catalog = queen_bee.get_blueprint_catalog()
    print("Available molecular blueprints:")
    for name, info in catalog.items():
        print(f"  🔹 {name}: {info['description']}")
        print(f"     Formula: {info['elements']}")
        print(f"     Stability: {info['stability']}")

    # Step 3: Synthesize a hexagonal molecule
    print_banner("Phase 3: Molecular Synthesis", "⚗️")

    component_name = "UserServiceCore"
    blueprint_name = "hexagonal_core"

    print(f"🧪 Synthesizing {component_name} using {blueprint_name} blueprint...")
    print("   Catalyst: Royal Jelly + Beekeeper Wisdom")
    print("   Temperature: 310K (optimal for aromatic stability)")

    # Build the component using Queen Bee
    result = await queen_bee.build_component(
        blueprint_name,
        component_name,
        {
            "temperature": 310.0,
            "catalysts": ["royal_jelly", "beekeeper_wisdom"],
            "additional_reactants": ["T"],  # Add extra transformation element
        },
    )

    if result.success:
        print("✅ Molecular synthesis successful!")
        print_result("Component ID", result.component_id)
        print_result("Stability Level", result.stability_report.stability_level.value)
        print_result(
            "Stability Score", f"{result.stability_report.stability_score:.1f}", "/100"
        )
        print_result(
            "Bond Energy", f"{result.stability_report.total_bond_energy:.1f}", " kJ/mol"
        )
        print_result(
            "Decomposition Risk", f"{result.stability_report.decomposition_risk:.2%}"
        )

        if result.stability_report.critical_bonds:
            print("\n   🔗 Critical Bonds:")
            for bond in result.stability_report.critical_bonds:
                print(f"      • {bond}")
    else:
        print("❌ Synthesis failed!")
        for warning in result.warnings:
            print(f"   ⚠️ {warning}")
        return

    # Step 4: Generate detailed honeyprint
    print_banner("Phase 4: Molecular Visualization", "🐝")

    print("🎨 Generating molecular honeyprint visualization...")

    # Create a custom honeyprint for our synthesized molecule
    adapters = ["REST_API", "GraphQL", "Database", "EventBus", "Auth", "Cache"]
    molecule = honeyprint_gen.create_hexagonal_molecule(component_name, adapters)

    # Add external connections
    external_connections = {
        "REST_API": "Mobile App",
        "Database": "PostgreSQL",
        "EventBus": "RabbitMQ",
        "Auth": "OAuth2 Provider",
    }
    molecule = honeyprint_gen.add_external_connections(molecule, external_connections)

    # Generate the beautiful SVG
    svg_content = honeyprint_gen.generate_svg(molecule)

    # Save the visualization
    output_file = "synthesized_molecule.svg"
    with open(output_file, "w") as f:
        f.write(svg_content)

    print(f"✅ Honeyprint saved to: {output_file}")
    print_result("Molecular Formula", molecule.molecular_formula)
    print_result("Atom Count", len(molecule.atoms))
    print_result("Bond Count", len(molecule.bonds))
    print_result("SVG Size", f"{len(svg_content)}", " characters")

    # Step 5: Chemical reaction analysis
    print_banner("Phase 5: Reaction Analysis", "⚗️")

    print("🔬 Analyzing chemical reactions used in synthesis...")

    # Show reactions that were executed
    for reaction_result in result.reaction_results:
        if reaction_result.success:
            print("✅ Successful reaction:")
            print(f"   Products: {', '.join(reaction_result.products_created)}")
            print(f"   Energy Released: {reaction_result.energy_released:.1f} kJ/mol")
            print(f"   Reaction Time: {reaction_result.reaction_time:.2f}s")

            if reaction_result.byproducts:
                print(f"   Byproducts: {', '.join(reaction_result.byproducts)}")

    # Step 6: System health analysis
    print_banner("Phase 6: System Health Analysis", "📊")

    health = queen_bee.get_system_health()
    print("🏥 Overall Hive System Health:")

    metrics = health["health_metrics"]
    print_result("System Stability", f"{metrics['stability_score']:.1f}", "/100")
    print_result("Complexity Index", f"{metrics['complexity_index']:.1f}")
    print_result("Coupling Coefficient", f"{metrics['coupling_coefficient']:.3f}")
    print_result("Aromatic Ratio", f"{metrics['aromatic_ratio']:.2%}")

    print("\n📈 Build Statistics:")
    print_result("Total Components", health["component_count"])
    print_result("Success Rate", f"{health['success_rate']:.2%}")
    print_result("Average Stability", f"{health['average_stability']:.1f}")

    # Step 7: Generate example honeyprint for comparison
    print_banner("Phase 7: Reference Molecule", "🔬")

    print("🧪 Generating reference molecule (based on original honeyprint.svg)...")
    reference_svg = create_example_honeyprint()

    with open("reference_honeyprint.svg", "w") as f:
        f.write(reference_svg)

    print("✅ Reference molecule saved to: reference_honeyprint.svg")
    print_result("Reference SVG Size", f"{len(reference_svg)}", " characters")

    # Step 8: Create molecular documentation
    print_banner("Phase 8: Molecular Documentation", "📚")

    doc_content = f"""# {component_name} - Molecular Architecture Report

## 🧬 Molecular Structure
- **Formula**: {molecule.molecular_formula}
- **Blueprint**: {blueprint_name}
- **Synthesis Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}

## 🔬 Stability Analysis
- **Stability Level**: {result.stability_report.stability_level.value}
- **Stability Score**: {result.stability_report.stability_score:.1f}/100
- **Bond Energy**: {result.stability_report.total_bond_energy:.1f} kJ/mol
- **Decomposition Risk**: {result.stability_report.decomposition_risk:.2%}

## 🎨 Visualization
![Molecular Structure](synthesized_molecule.svg)

## 💡 Recommendations
{chr(10).join(f"- {rec}" for rec in result.recommendations)}

## ⚗️ Synthesis Details
- **Catalysts Used**: Royal Jelly, Beekeeper Wisdom
- **Reaction Temperature**: 310K
- **Energy Released**: {sum(r.energy_released for r in result.reaction_results):.1f} kJ/mol
- **Synthesis Time**: {sum(r.reaction_time for r in result.reaction_results):.2f}s

---
*Generated by Queen Bee Molecular Architecture System* 🐝👑
"""

    with open("molecular_report.md", "w") as f:
        f.write(doc_content)

    print("✅ Molecular documentation saved to: molecular_report.md")

    # Final summary
    print_banner("🎉 SYNTHESIS COMPLETE!", "✨")

    print("🧪 Successfully demonstrated molecular architecture system!")
    print("\n📁 Generated Files:")
    print("   • synthesized_molecule.svg - Your custom molecular structure")
    print("   • reference_honeyprint.svg - Reference benzene-like structure")
    print("   • molecular_report.md - Complete molecular analysis")
    print("   • chemical_registry.db - Component database")

    print("\n🚀 Next Steps:")
    print("   • Open the SVG files in a browser to see the beautiful molecules")
    print("   • Run 'python molecular_demo.py' again to synthesize more molecules")
    print("   • Try the CLI: python genesis-engine/main.py molecular lab")

    print("\n✨ The future of architecture is molecular! 🧬🐝")


if __name__ == "__main__":
    asyncio.run(molecular_growth_demo())
