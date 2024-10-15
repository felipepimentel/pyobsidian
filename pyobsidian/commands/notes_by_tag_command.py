from typing import Dict, List

import click

from ..core import Note, Vault, obsidian_context
from ..ui_handler import handle_command_action


def get_notes_by_tag(vault: "Vault") -> Dict[str, List[Note]]:
    """
    Get a dictionary of tags and their associated notes.

    Args:
        vault (Vault): The Obsidian vault to search for notes and tags.

    Returns:
        Dict[str, List[Note]]: A dictionary where keys are tags and values are lists of notes with that tag.
    """
    notes_by_tag: Dict[str, List[Note]] = {}
    for note in vault.get_all_notes():
        for tag in note.tags:
            if tag not in notes_by_tag:
                notes_by_tag[tag] = []
            notes_by_tag[tag].append(note)
    return notes_by_tag


@click.command()
@click.option("--tag", help="Specific tag to filter notes (optional)")
def notes_by_tag_command(tag: str = None) -> None:
    """
    Display notes grouped by tags or filtered by a specific tag.

    Args:
        tag (str, optional): Specific tag to filter notes. If not provided, all tags and their notes are displayed.
    """
    notes_by_tag = get_notes_by_tag(obsidian_context.vault)

    handle_command_action(
        items=notes_by_tag,
        item_type="notes_by_tag",
        display_format="tags_and_notes",
        empty_text="No tags or notes found in the vault",
        title="Notes by Tag",
        filter_tag=tag,
    )


def register_command(cli: click.Group) -> None:
    """Register the notes by tag command to the CLI group."""
    cli.add_command(notes_by_tag_command, name="notes-by-tag")
