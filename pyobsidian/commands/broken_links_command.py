"""Broken links command for PyObsidian."""
from typing import Dict, List, Tuple

import click

from ..core import Note, Link, obsidian_context
from ..ui_handler import display_broken_links


def broken_links_impl() -> List[Note]:
    """Find notes with broken links."""
    broken_notes = []
    all_notes = obsidian_context.vault.get_all_notes()
    note_paths = {note.path for note in all_notes}
    
    for note in all_notes:
        for link in note.links:
            target_path = f"{link.target}.md"
            if target_path not in note_paths:
                broken_notes.append(note)
                break
    return broken_notes


@click.command()
def broken_links() -> None:
    """Find broken links in notes."""
    notes_with_broken_links = []
    for note in obsidian_context.vault.notes.values():
        broken_links = []
        for link in note.links:
            if not obsidian_context.vault.note_exists(link.target):
                broken_links.append(link)
        if broken_links:
            notes_with_broken_links.append((note, broken_links))
    
    display_broken_links(notes_with_broken_links)


def register_command(cli: click.Group) -> None:
    """Register the broken-links command to the CLI group."""
    cli.add_command(broken_links)
