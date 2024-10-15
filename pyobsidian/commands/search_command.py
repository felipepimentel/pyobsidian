from typing import List

import click

from ..core import Note, Vault, obsidian_context
from ..ui_handler import handle_command_action


def search_notes(vault: "Vault", keyword: str) -> List[Note]:
    """Search for notes containing the given keyword."""
    return [
        note
        for note in vault.get_all_notes()
        if keyword.lower() in note.content.lower()
    ]


@click.command()
@click.argument("keyword", type=str)
@click.option("--delete", is_flag=True, help="Delete the identified notes")
def search_command(keyword: str, delete: bool) -> None:
    """Search for notes containing a specific word."""
    matching_notes = search_notes(obsidian_context.vault, keyword)

    handle_command_action(items=matching_notes, delete=delete)


def register_command(cli: click.Group) -> None:
    """Register the search command to the CLI group."""
    cli.add_command(search_command, name="search")
