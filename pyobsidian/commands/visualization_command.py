"""Visualization commands for PyObsidian."""
import click

from ..core import obsidian_context
from ..ui_handler import display_success, display_error
from .base_command import BaseCommand


@click.command(cls=BaseCommand, name="visualize-graph")
@click.option("--output", default="graph.html", help="Output file path")
def visualize_graph(output: str) -> None:
    """Create a graph visualization of note relationships."""
    try:
        obsidian_context.vault.create_graph_visualization(output)
        display_success("Graph visualization created successfully.")
    except Exception as e:
        display_error(f"Failed to create graph visualization: {str(e)}")


@click.command(cls=BaseCommand, name="visualize-tags")
@click.option("--output", default="tags.html", help="Output file path")
def visualize_tags(output: str) -> None:
    """Create a tag cloud visualization."""
    try:
        obsidian_context.vault.create_tag_cloud(output)
        display_success("Tag cloud visualization created successfully.")
    except Exception as e:
        display_error(f"Failed to create tag cloud visualization: {str(e)}")


def register_command(cli: click.Group) -> None:
    """Register the visualization commands to the CLI group."""
    cli.add_command(visualize_graph)
    cli.add_command(visualize_tags)
