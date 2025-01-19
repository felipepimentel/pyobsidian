"""Small notes command for PyObsidian."""
from typing import List

import click

from ..core import Note, obsidian_context
from ..ui_handler import display_notes


@click.command()
@click.option("--min-words", default=5, help="Minimum word count threshold (default: 5)")
def small_notes(min_words: int = 5) -> None:
    """Find notes with few words (below the specified threshold)."""
    small_notes = []
    
    for note in obsidian_context.vault.get_all_notes():
        # Only include notes that have content but are below the threshold
        if 0 < note.word_count < min_words:
            small_notes.append(note)
    
    # Sort small notes by path for consistent output
    small_notes.sort(key=lambda x: x.path)
    
    # Display results
    display_notes(small_notes, f"Notes with fewer than {min_words} words")


def register_command(cli: click.Group) -> None:
    """Register the small-notes command to the CLI group."""
    cli.add_command(small_notes)
