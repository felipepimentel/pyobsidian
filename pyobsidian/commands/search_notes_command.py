"""Search notes command."""
import click

from ..core import obsidian_context
from ..ui_handler import display_notes


@click.command(name="search-notes")
@click.argument("query")
@click.option("--case-sensitive", is_flag=True, help="Enable case-sensitive search")
def search_notes(query: str, case_sensitive: bool = False) -> None:
    """Search for notes containing a query string."""
    notes = obsidian_context.vault.search_notes(query, case_sensitive)
    display_notes(notes, f"Search Results for '{query}'")


def register_command(cli: click.Group) -> None:
    """Register the search-notes command to the CLI group."""
    cli.add_command(search_notes)
