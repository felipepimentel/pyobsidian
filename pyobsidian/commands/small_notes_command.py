"""Small notes command for PyObsidian."""
from typing import List

import click

from ..core import Note, obsidian_context
from ..ui_handler import display_small_notes


@click.command()
def small_notes() -> None:
    """Find notes with fewer than 5 words and no title."""
    notes = obsidian_context.vault.get_all_notes()
    small = [note for note in notes if note.word_count < 5 and not note.title]
    display_small_notes(small)


def register_command(cli: click.Group) -> None:
    """Register the small-notes command to the CLI group."""
    cli.add_command(small_notes, name="small-notes")
