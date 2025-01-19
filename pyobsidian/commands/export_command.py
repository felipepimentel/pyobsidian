"""Export command for PyObsidian."""
import click

from ..core import obsidian_context
from ..ui_handler import display_success, display_error
from .base_command import BaseCommand


@click.command(cls=BaseCommand, name="export")
@click.option("--format", type=click.Choice(["markdown", "html"]), default="markdown", help="Export format")
@click.option("--output", default="export", help="Output directory")
def export_notes(format: str, output: str) -> None:
    """Export notes to the specified format."""
    try:
        if format == "markdown":
            obsidian_context.vault.export_to_markdown(output)
            display_success(f"Notes exported to markdown in {output}")
        else:
            obsidian_context.vault.export_to_html(output)
            display_success(f"Notes exported to HTML in {output}")
    except Exception as e:
        display_error(f"Failed to export notes: {str(e)}")


def register_command(cli: click.Group) -> None:
    """Register the export command to the CLI group."""
    cli.add_command(export_notes)
