#!/usr/bin/env python
import click

# Import the "organelles" of our Genesis Engine
from aggregates.compiler_aggregate import CompilerAggregate, HatchCommand
from transformations.code_generator import CodeGenerationTransformation
from connectors.cli_connector import CliConnector
from connectors.file_writer_connector import FileWriterConnector

# Import molecular chemistry CLI commands
from molecular_cli import molecular

# --- Configuration ---
HIVE_ROOT = "hive/components"
TEMPLATE_DIR = "tRNA"


# --- The main application wiring ---
# This is where we instantiate our components and wire them together.
# This setup is our dependency injection container, in a sense.

# 1. Create the core components
compiler_aggregate = CompilerAggregate()
code_generator = CodeGenerationTransformation(template_dir=TEMPLATE_DIR)
file_writer = FileWriterConnector()


# 2. Define the flow of control (the "central nervous system")
def handle_hatch_command(command: HatchCommand):
    """
    This function orchestrates the entire process, acting as a simple
    application service or command bus.
    """
    # First, the command is handled by the aggregate
    events = compiler_aggregate.handle_hatch_command(command, HIVE_ROOT)

    # The resulting events are then processed by transformations and connectors
    for event in events:
        if event.event_type == "ComponentHatchingInitiated":
            # The code generator processes the event to create the code
            generated_code_events = code_generator.process(event)
            # The file writer connector handles the generated code
            file_writer.handle(generated_code_events)


# 3. Create the primary (driving) connector and pass it the command handler
cli_connector = CliConnector(command_handler=handle_hatch_command)


# --- CLI Definition ---
# The CLI definition now only deals with the user interface and calling the connector.


@click.group()
def cli():
    """
    🐝 The Genesis Engine - Molecular Architecture for the Hive

    Build software using nature-inspired molecular chemistry principles.
    Traditional ATCG patterns + Advanced molecular analysis and visualization.
    """
    pass


@cli.group(help="Scaffolds a new component pattern.")
def hatch():
    pass


@hatch.command(
    name="command", help="Scaffolds a 'Handle Command' pattern (C -> A -> G)."
)
@click.argument("component_name")
def hatch_command_cli(component_name):
    cli_connector.hatch("command", component_name)


@hatch.command(name="query", help="Scaffolds a 'Query Data' pattern (C -> T -> C).")
@click.argument("component_name")
def hatch_query_cli(component_name):
    cli_connector.hatch("query", component_name)


@hatch.command(
    name="event", help="Scaffolds a 'React to Event' pattern (G -> C -> A -> G)."
)
@click.argument("component_name")
def hatch_event_cli(component_name):
    cli_connector.hatch("event", component_name)


@hatch.command(
    name="immune", help="Scaffolds an 'Immune Response' pattern (G -> C -> A -> C)."
)
@click.argument("component_name")
def hatch_immune_cli(component_name):
    cli_connector.hatch("immune", component_name)


# Placeholder for the spin command
@cli.command(
    help="Adds testing or other infrastructure to a component (Under Construction)."
)
@click.argument("component_name")
def spin(component_name):
    cli_connector.spin(component_name)


# Add molecular chemistry commands to main CLI
cli.add_command(molecular)


# Add a quick demo command
@cli.command()
def demo():
    """🎭 Run a quick demonstration of the molecular chemistry system"""
    click.echo("🧪 Genesis Engine - Molecular Chemistry Demo")
    click.echo("=" * 50)

    click.echo("\n🐝 Available Commands:")
    click.echo(
        "  genesis-engine hatch command <name>     - Traditional component scaffolding"
    )
    click.echo(
        "  genesis-engine molecular queen build    - Molecular component building"
    )
    click.echo(
        "  genesis-engine molecular honeyprint     - SVG visualization generation"
    )
    click.echo(
        "  genesis-engine molecular react run      - Chemical reaction execution"
    )
    click.echo("  genesis-engine molecular analyze        - Stability analysis")
    click.echo("  genesis-engine molecular registry       - Component database")
    click.echo("  genesis-engine molecular lab            - Interactive web lab")

    click.echo("\n🧬 Try this:")
    click.echo("  python -m genesis-engine molecular queen blueprints")
    click.echo(
        "  python -m genesis-engine molecular queen build hexagonal_core MyService"
    )
    click.echo("  python -m genesis-engine molecular lab")

    click.echo("\n✨ The future of architecture is molecular! 🧪🐝")


if __name__ == "__main__":
    # This check ensures that if this file is imported, the CLI doesn't run.
    # It only runs when executed directly.
    cli()
