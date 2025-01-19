"""Orphan links command for PyObsidian."""
from typing import List
import os

import click

from ..core import Note, obsidian_context
from ..ui_handler import display_orphan_notes


def orphan_notes_impl(include_empty: bool = False) -> List[Note]:
    """Find orphaned notes (not linked from anywhere)."""
    all_notes = obsidian_context.vault.get_all_notes()
    linked_paths = set()
    
    # Collect all linked note paths
    for note in all_notes:
        for link in note.links:
            linked_paths.add(f"{link.target}.md")
    
    # Find notes that are not linked from anywhere
    orphaned_notes = []
    for note in all_notes:
        if note.path not in linked_paths:
            if include_empty or note.word_count > 0:
                orphaned_notes.append(note)
    
    return orphaned_notes


@click.command()
@click.option("--include-empty", is_flag=True, help="Include empty notes in the results.")
def orphan_notes(include_empty: bool = False) -> None:
    """Find notes that are not linked from any other note."""
    linked_notes = set()
    orphan_notes = []

    # First, collect all notes that are linked from other notes
    for note in obsidian_context.vault.notes.values():
        for link in note.links:
            # Add both with and without .md extension
            target_name = link.target
            linked_notes.add(target_name)
            linked_notes.add(f"{target_name}.md")
            if target_name.endswith(".md"):
                linked_notes.add(target_name[:-3])

    # Then find notes that are not linked from anywhere
    for note in obsidian_context.vault.notes.values():
        note_name = os.path.basename(note.path)
        note_name_no_ext = os.path.splitext(note_name)[0]
        
        # Check if the note is not linked (with or without .md extension)
        if note_name not in linked_notes and note_name_no_ext not in linked_notes:
            # Include empty notes only if include_empty is True
            if include_empty and note.word_count == 0:
                orphan_notes.append(note)
            # Include non-empty notes regardless of include_empty flag
            elif note.word_count > 0:
                orphan_notes.append(note)

    # Sort orphan notes by path
    orphan_notes.sort(key=lambda x: x.path)

    # Display results
    if not orphan_notes:
        click.echo("No orphan notes found.")
    else:
        display_orphan_notes(orphan_notes)


def register_command(cli: click.Group) -> None:
    """Register the orphan-notes command to the CLI group."""
    cli.add_command(orphan_notes)
