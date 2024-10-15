import os
from typing import List, Tuple

import click

from ..core import Note, Vault, obsidian_context
from ..ui_handler import handle_command_action


def get_broken_links(vault: "Vault") -> List[Tuple[Note, str]]:
    broken_links = []
    all_note_filenames = {
        os.path.basename(note.filename) for note in vault.get_all_notes()
    }

    for note in vault.get_all_notes():
        for link in note.links:
            if link not in all_note_filenames:
                broken_links.append((note, link))
    return broken_links


@click.command()
@click.option("--delete", is_flag=True, help="Delete the broken links")
def broken_links_command(delete: bool) -> None:
    """Identify broken links in notes."""
    broken_links = get_broken_links(obsidian_context.vault)

    handle_command_action(items=broken_links, delete=delete)


def register_command(cli: click.Group) -> None:
    """Register the broken links command to the CLI group."""
    cli.add_command(broken_links_command, name="broken-links")
