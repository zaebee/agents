#!/usr/bin/env python3
"""
Molecular Chemistry CLI - Extended Genesis Engine Interface
Adds molecular chemistry commands to the Genesis Engine CLI.

This extends the original CLI with advanced molecular architecture commands
for honeyprint generation, stability analysis, and chemical reactions.
"""

import click
import asyncio
import json
from pathlib import Path

# Import our molecular components
from .aggregates.queen_bee import QueenBee
from .transformations.honeyprint_generator import (
    HoneyprintGenerator,
    create_example_honeyprint,
)
from .transformations.reaction_engine import ReactionEngine
from .aggregates.molecular_analyzer import MolecularAnalyzer
from .connectors.chemical_registry import (
    ChemicalRegistry,
    SearchQuery,
    ComponentStability,
)

# Global instances (initialized on first use)
_queen_bee: QueenBee = None
_honeyprint_generator: HoneyprintGenerator = None
_reaction_engine: ReactionEngine = None
_molecular_analyzer: MolecularAnalyzer = None
_chemical_registry: ChemicalRegistry = None


def get_queen_bee() -> QueenBee:
    """Get or create Queen Bee instance"""
    global _queen_bee
    if _queen_bee is None:
        _queen_bee = QueenBee()
    return _queen_bee


def get_honeyprint_generator() -> HoneyprintGenerator:
    """Get or create Honeyprint Generator instance"""
    global _honeyprint_generator
    if _honeyprint_generator is None:
        _honeyprint_generator = HoneyprintGenerator()
    return _honeyprint_generator


def get_reaction_engine() -> ReactionEngine:
    """Get or create Reaction Engine instance"""
    global _reaction_engine
    if _reaction_engine is None:
        _reaction_engine = ReactionEngine()
    return _reaction_engine


def get_molecular_analyzer() -> MolecularAnalyzer:
    """Get or create Molecular Analyzer instance"""
    global _molecular_analyzer
    if _molecular_analyzer is None:
        _molecular_analyzer = MolecularAnalyzer()
    return _molecular_analyzer


def get_chemical_registry() -> ChemicalRegistry:
    """Get or create Chemical Registry instance"""
    global _chemical_registry
    if _chemical_registry is None:
        _chemical_registry = ChemicalRegistry()
    return _chemical_registry


@click.group()
def molecular():
    """
    🧪 Molecular Chemistry Commands
    Advanced molecular architecture design and analysis tools.
    """
    pass


# --- QUEEN BEE COMMANDS ---


@molecular.group()
def queen():
    """👑 Queen Bee - Master orchestrator commands"""
    pass


@queen.command()
@click.argument("blueprint_name")
@click.argument("component_name")
@click.option(
    "--temperature", type=float, default=298.0, help="Reaction temperature (K)"
)
@click.option("--pressure", type=float, default=1.0, help="Reaction pressure (atm)")
@click.option("--catalyst", multiple=True, help="Catalysts to use")
@click.option("--params", type=str, help="JSON string of additional parameters")
def build(blueprint_name, component_name, temperature, pressure, catalyst, params):
    """Build a molecular component from an architectural blueprint"""

    async def _build():
        queen = get_queen_bee()

        # Parse additional parameters
        custom_params = {"temperature": temperature, "pressure": pressure}
        if catalyst:
            custom_params["catalysts"] = list(catalyst)
        if params:
            try:
                additional = json.loads(params)
                custom_params.update(additional)
            except json.JSONDecodeError:
                click.echo("❌ Invalid JSON in params parameter", err=True)
                return

        click.echo(
            f"👑 Building component '{component_name}' using blueprint '{blueprint_name}'..."
        )

        result = await queen.build_component(
            blueprint_name, component_name, custom_params
        )

        if result.success:
            click.echo("✅ Component built successfully!")
            click.echo(f"   Component ID: {result.component_id}")
            click.echo(f"   Stability: {result.stability_report.stability_level.value}")
            click.echo(f"   Score: {result.stability_report.stability_score:.1f}/100")
            click.echo(
                f"   Bond Energy: {result.stability_report.total_bond_energy:.1f} kJ/mol"
            )

            if result.recommendations:
                click.echo("📋 Recommendations:")
                for rec in result.recommendations[:3]:  # Show top 3
                    click.echo(f"   • {rec}")
        else:
            click.echo("❌ Component build failed!")
            for warning in result.warnings:
                click.echo(f"   ⚠️ {warning}")

    asyncio.run(_build())


@queen.command()
def blueprints():
    """List available architectural blueprints"""
    queen = get_queen_bee()
    catalog = queen.get_blueprint_catalog()

    click.echo("📋 Available Architectural Blueprints:\n")

    for name, info in catalog.items():
        click.echo(f"🔹 {click.style(name, fg='blue', bold=True)}")
        click.echo(f"   {info['description']}")
        click.echo(f"   Elements: {info['elements']}")
        click.echo(f"   Stability: {info['stability']}")
        click.echo()


@queen.command()
def health():
    """Show system health and metrics"""
    queen = get_queen_bee()
    health_data = queen.get_system_health()

    click.echo("📊 Hive System Health Report\n")

    metrics = health_data["health_metrics"]
    stability_text = f"{metrics['stability_score']:.1f}/100"
    color = "green" if metrics["stability_score"] > 80 else "yellow"
    click.echo(f"Overall Stability Score: {click.style(stability_text, fg=color)}")
    click.echo(f"Complexity Index: {metrics['complexity_index']:.1f}")
    click.echo(f"Coupling Coefficient: {metrics['coupling_coefficient']:.3f}")
    click.echo(f"Aromatic Ratio: {metrics['aromatic_ratio']:.2%}")

    click.echo("\n📈 Build Statistics:")
    click.echo(f"Total Components: {health_data['component_count']}")
    click.echo(f"Total Builds: {health_data['total_builds']}")
    click.echo(f"Recent Builds (7 days): {health_data['recent_builds']}")
    click.echo(f"Success Rate: {health_data['success_rate']:.2%}")
    click.echo(f"Average Stability: {health_data['average_stability']:.1f}")


# --- HONEYPRINT COMMANDS ---


@molecular.group()
def honeyprint():
    """🐝 Honeyprint - Molecular visualization commands"""
    pass


@honeyprint.command()
@click.option("--output", "-o", default="honeyprint.svg", help="Output SVG file")
@click.option("--core", default="Core", help="Core component name")
@click.option(
    "--adapters",
    default="REST,gRPC,SQL,Events,Auth,CLI",
    help="Comma-separated adapter list",
)
@click.option("--width", default=600, help="SVG width")
@click.option("--height", default=500, help="SVG height")
def generate(output, core, adapters, width, height):
    """Generate a honeyprint SVG visualization"""
    generator = get_honeyprint_generator()
    generator.width = width
    generator.height = height

    adapter_list = [a.strip() for a in adapters.split(",")]

    click.echo(
        f"🐝 Generating honeyprint for {core} with {len(adapter_list)} adapters..."
    )

    # Create hexagonal molecule
    molecule = generator.create_hexagonal_molecule(core, adapter_list)

    # Generate SVG
    svg_content = generator.generate_svg(molecule)

    # Write to file
    with open(output, "w") as f:
        f.write(svg_content)

    click.echo(f"✅ Honeyprint saved to {output}")
    click.echo(f"   Formula: {molecule.molecular_formula}")


@honeyprint.command()
def example():
    """Generate an example honeyprint (based on original design)"""
    click.echo("🐝 Generating example honeyprint...")

    svg_content = create_example_honeyprint()

    with open("example_honeyprint.svg", "w") as f:
        f.write(svg_content)

    click.echo("✅ Example honeyprint saved to example_honeyprint.svg")


# --- REACTION COMMANDS ---


@molecular.group()
def react():
    """⚗️ Reaction Engine - Chemical reaction commands"""
    pass


@react.command()
@click.argument("reactants", nargs=-1)
@click.option("--catalyst", multiple=True, help="Catalysts to use")
@click.option(
    "--temperature", type=float, default=298.0, help="Reaction temperature (K)"
)
@click.option("--pressure", type=float, default=1.0, help="Reaction pressure (atm)")
def run(reactants, catalyst, temperature, pressure):
    """Run a chemical reaction with specified reactants"""
    engine = get_reaction_engine()

    if not reactants:
        click.echo("❌ No reactants specified!", err=True)
        return

    reactant_list = list(reactants)
    catalyst_list = list(catalyst) if catalyst else []

    click.echo(f"⚗️ Finding reactions for: {' + '.join(reactant_list)}")
    if catalyst_list:
        click.echo(f"   Catalysts: {', '.join(catalyst_list)}")

    # Find possible reactions
    possible = engine.find_possible_reactions(reactant_list, catalyst_list)

    if not possible:
        click.echo("❌ No reactions possible with these reactants")
        return

    click.echo(f"✅ Found {len(possible)} possible reactions:")

    for i, reaction in enumerate(possible, 1):
        click.echo(f"\n{i}. {reaction.name}: {reaction}")

        # Execute the reaction
        result = engine.execute_reaction(
            reaction, reactant_list, catalyst_list, temperature, pressure
        )

        if result.success:
            click.echo(f"   ✅ Success! Products: {', '.join(result.products_created)}")
            click.echo(f"   ⚡ Energy released: {result.energy_released:.1f} kJ/mol")
            click.echo(f"   ⏱️ Reaction time: {result.reaction_time:.2f}s")

            if result.byproducts:
                click.echo(f"   🧪 Byproducts: {', '.join(result.byproducts)}")
        else:
            click.echo(f"   ❌ Failed: {', '.join(result.side_effects)}")


@react.command()
def list():
    """List all known chemical reactions"""
    engine = get_reaction_engine()

    click.echo("⚗️ Known Chemical Reactions:\n")

    for name, reaction in engine._known_reactions.items():
        click.echo(f"🔹 {click.style(name, fg='blue', bold=True)}")
        click.echo(f"   {reaction}")
        click.echo(f"   Type: {reaction.reaction_type.value}")
        click.echo(f"   Activation Energy: {reaction.activation_energy:.1f} kJ/mol")
        if reaction.catalysts:
            click.echo(f"   Catalysts: {', '.join(reaction.catalysts)}")
        click.echo()


@react.command()
def stats():
    """Show reaction engine statistics"""
    engine = get_reaction_engine()
    stats = engine.get_reaction_statistics()

    if not stats:
        click.echo("📊 No reactions have been executed yet")
        return

    click.echo("📊 Reaction Engine Statistics:\n")

    click.echo(f"Total Reactions: {stats['total_reactions']}")
    click.echo(f"Success Rate: {stats['success_rate']:.2%}")
    click.echo(f"Total Energy Consumed: {stats['total_energy_consumed']:.1f} kJ/mol")
    click.echo(f"Total Energy Released: {stats['total_energy_released']:.1f} kJ/mol")
    click.echo(f"Net Energy: {stats['net_energy']:.1f} kJ/mol")
    click.echo(f"Average Reaction Time: {stats['avg_reaction_time']:.2f}s")


# --- ANALYSIS COMMANDS ---


@molecular.group()
def analyze():
    """🔬 Molecular Analysis - Stability and structure analysis"""
    pass


@analyze.command()
@click.argument("component_name")
@click.argument("formula")
@click.option(
    "--connections", help="Comma-separated connection pairs (from:to,from:to)"
)
def stability(component_name, formula, connections):
    """Analyze molecular stability of a component"""
    analyzer = get_molecular_analyzer()

    # Parse connections
    connection_list = []
    if connections:
        pairs = connections.split(",")
        for pair in pairs:
            if ":" in pair:
                from_comp, to_comp = pair.strip().split(":", 1)
                connection_list.append((from_comp.strip(), to_comp.strip()))

    click.echo(f"🔬 Analyzing stability for {component_name} ({formula})...")

    report = analyzer.analyze_molecular_stability(
        component_name, formula, connection_list
    )

    click.echo("\n📊 Stability Analysis Results:")
    stability_color = "green" if report.stability_score > 80 else "yellow"
    click.echo(
        f"   Stability Level: {click.style(report.stability_level.value, fg=stability_color)}"
    )
    click.echo(f"   Stability Score: {report.stability_score:.1f}/100")
    click.echo(f"   Total Bond Energy: {report.total_bond_energy:.1f} kJ/mol")
    click.echo(f"   Decomposition Risk: {report.decomposition_risk:.2%}")

    if report.critical_bonds:
        click.echo("\n🔗 Critical Bonds:")
        for bond in report.critical_bonds:
            click.echo(f"   • {bond}")

    if report.recommendations:
        click.echo("\n💡 Recommendations:")
        for rec in report.recommendations:
            click.echo(f"   • {rec}")


# --- REGISTRY COMMANDS ---


@molecular.group()
def registry():
    """📚 Chemical Registry - Component database commands"""
    pass


@registry.command()
@click.option("--name", help="Search by name pattern")
@click.option("--formula", help="Search by exact molecular formula")
@click.option(
    "--stability",
    type=click.Choice(
        ["experimental", "stable", "deprecated", "radioactive", "aromatic"]
    ),
    help="Filter by stability",
)
@click.option("--limit", default=10, help="Maximum results to show")
def search(name, formula, stability, limit):
    """Search components in the chemical registry"""
    registry = get_chemical_registry()

    # Build search query
    query = SearchQuery()
    if name:
        query.name_pattern = name
    if formula:
        query.molecular_formula = formula
    if stability:
        query.stability = ComponentStability(stability)

    click.echo("🔍 Searching chemical registry...")

    results = registry.search_components(query)

    if not results:
        click.echo("❌ No components found matching criteria")
        return

    click.echo(
        f"✅ Found {len(results)} components (showing top {min(limit, len(results))}):\n"
    )

    for i, comp in enumerate(results[:limit], 1):
        click.echo(f"{i}. {click.style(comp.name, fg='blue', bold=True)}")
        click.echo(f"   Formula: {comp.molecular_formula}")
        click.echo(f"   Stability: {comp.stability.value}")
        click.echo(f"   Bond Energy: {comp.bond_energy:.1f} kJ/mol")
        click.echo(f"   Usage: {comp.usage_count} times")
        click.echo(f"   Created: {comp.creation_date.strftime('%Y-%m-%d')}")
        click.echo()


@registry.command()
@click.option("--limit", default=10, help="Number of top components to show")
def popular():
    """Show most popular components by usage"""
    registry = get_chemical_registry()

    rankings = registry.get_popularity_rankings(limit)

    if not rankings:
        click.echo("📊 No usage data available yet")
        return

    click.echo(f"🏆 Top {len(rankings)} Popular Components:\n")

    for i, (comp, usage_count) in enumerate(rankings, 1):
        click.echo(
            f"{i}. {click.style(comp.name, fg='blue', bold=True)} - {usage_count} uses"
        )
        click.echo(f"   {comp.molecular_formula} ({comp.stability.value})")
        click.echo()


@registry.command()
def trends():
    """Show composition trends across all components"""
    registry = get_chemical_registry()

    trends = registry.analyze_composition_trends()

    click.echo("📈 Element Composition Trends:\n")

    # Total element usage
    total = trends["total_elements"]
    total_sum = sum(total.values())

    if total_sum > 0:
        click.echo("Overall Element Distribution:")
        for element, count in total.items():
            percentage = count / total_sum * 100
            click.echo(f"  {element}: {count} atoms ({percentage:.1f}%)")

    # By stability
    click.echo("\nBy Stability Level:")
    for stability, elements in trends["by_stability"].items():
        element_sum = sum(elements.values())
        if element_sum > 0:
            click.echo(f"  {stability.title()}:")
            for element, count in elements.items():
                if count > 0:
                    click.echo(f"    {element}: {count} atoms")


@registry.command()
@click.argument("output_file")
@click.option(
    "--format", type=click.Choice(["json", "csv"]), default="json", help="Export format"
)
def export(output_file, format):
    """Export registry to file"""
    registry = get_chemical_registry()

    click.echo(f"📁 Exporting registry to {output_file} ({format} format)...")

    success = registry.export_registry(output_file, format)

    if success:
        click.echo("✅ Export completed successfully")
    else:
        click.echo("❌ Export failed", err=True)


# --- LAB COMMAND ---


@molecular.command()
@click.option("--port", default=8000, help="Web server port")
def lab(port):
    """🧪 Start the interactive chemistry laboratory web interface"""
    import webbrowser

    # Import web server
    try:
        from .web_lab_server import start_chemistry_lab_server
    except ImportError:
        from web_lab_server import start_chemistry_lab_server

    # Find the web lab directory
    lab_dir = Path(__file__).parent.parent / "web_lab"

    if not lab_dir.exists():
        click.echo("❌ Chemistry lab web interface not found!", err=True)
        return

    click.echo(f"🧪 Starting Chemistry Laboratory with API on port {port}...")
    click.echo(f"📄 Open http://localhost:{port}/chemistry_lab.html")

    # Try to open browser automatically
    try:
        webbrowser.open(f"http://localhost:{port}/chemistry_lab.html")
    except:
        pass

    click.echo("Press Ctrl+C to stop the server")

    try:
        start_chemistry_lab_server(port, lab_dir)
    except KeyboardInterrupt:
        click.echo("\n🛑 Chemistry Laboratory stopped")
    except Exception as e:
        click.echo(f"❌ Failed to start web server: {e}", err=True)


# Add molecular commands to main CLI if this is run directly
if __name__ == "__main__":
    molecular()
