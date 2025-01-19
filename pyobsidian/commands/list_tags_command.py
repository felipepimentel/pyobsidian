"""List tags command."""
import click

from ..core import obsidian_context
from ..ui_handler import display_tags


@click.command(name="list-tags")
def list_tags() -> None:
    """List all tags in the vault."""
    tag_counts = obsidian_context.vault.get_all_tags()
    display_tags(tag_counts)

def register_command(cli: click.Group) -> None:
    """Register the list-tags command to the CLI group."""
    cli.add_command(list_tags)
