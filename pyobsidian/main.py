"""Main entry point for PyObsidian CLI."""
import click

from .core import obsidian_context
from .commands import (
    search_notes_command,
    list_tags_command,
    notes_by_tag_command,
    empty_notes_command,
    small_notes_command,
    empty_folders_command,
    broken_links_command,
    orphan_links_command,
    tag_management_command,
    visualization_command,
    data_management_command,
    export_command,
)

@click.group()
def cli() -> None:
    """PyObsidian CLI - A command-line tool for managing Obsidian vaults."""
    pass

def main() -> None:
    """Register commands and run the CLI."""
    # Register all commands
    search_notes_command.register_command(cli)
    list_tags_command.register_command(cli)
    notes_by_tag_command.register_command(cli)
    empty_notes_command.register_command(cli)
    small_notes_command.register_command(cli)
    empty_folders_command.register_command(cli)
    broken_links_command.register_command(cli)
    orphan_links_command.register_command(cli)
    tag_management_command.register_command(cli)
    visualization_command.register_command(cli)
    data_management_command.register_command(cli)
    export_command.register_command(cli)
    
    cli() 