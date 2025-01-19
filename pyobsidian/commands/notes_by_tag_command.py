"""Notes by tag command."""
import click

from ..core import obsidian_context
from ..ui_handler import display_notes


@click.command(name="notes-by-tag")
@click.argument("tag")
def notes_by_tag(tag: str) -> None:
    """List notes with a specific tag."""
    notes = obsidian_context.vault.get_notes_by_tag(tag)
    display_notes(notes, f"Notes with tag '#{tag}'")


def register_command(cli: click.Group) -> None:
    """Register the notes-by-tag command to the CLI group."""
    cli.add_command(notes_by_tag)
