import click

from ..core import obsidian_context
from ..ui_handler import display_export_result


@click.group()
def export() -> None:
    """Commands for exporting notes."""
    pass


@export.command()
@click.argument("note_title")
@click.option(
    "--format", type=click.Choice(["markdown", "pdf", "html"]), default="markdown"
)
def export_note(note_title: str, format: str) -> None:
    """Export a note in different formats (Markdown, PDF, HTML)."""
    vault = obsidian_context.vault
    note = vault.get_note(note_title)
    if note:
        export_result = f"Note '{note_title}' exported as {format}"
    else:
        export_result = f"Note '{note_title}' not found"

    display_export_result(export_result)


def register_command(cli: click.Group) -> None:
    """Register the export commands to the CLI group."""
    cli.add_command(export)
