"""Empty notes command for PyObsidian."""
from typing import List

import click

from ..core import Note, obsidian_context
from ..ui_handler import display_empty_notes


def empty_notes_impl() -> List[Note]:
    """Find empty notes in the vault."""
    empty_notes = []
    for note in obsidian_context.vault.get_all_notes():
        if note.word_count == 0:
            empty_notes.append(note)
    return empty_notes


@click.command(name="empty-notes")
def empty_notes() -> None:
    """List empty notes in the vault."""
    empty_notes = empty_notes_impl()
    display_empty_notes(empty_notes)


def register_command(cli: click.Group) -> None:
    """Register the empty-notes command to the CLI group."""
    cli.add_command(empty_notes)
