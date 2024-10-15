from typing import List

import click

from ..core import Note, Vault, obsidian_context
from ..ui_handler import handle_command_action


def get_empty_notes(vault: "Vault", threshold: int) -> List[Note]:
    return [note for note in vault.get_all_notes() if note.file_size < threshold]


@click.command()
@click.option("--delete", is_flag=True, help="Delete the identified empty notes")
def empty_notes_command(delete: bool) -> None:
    """Identify empty notes."""
    empty_notes = get_empty_notes(
        obsidian_context.vault, obsidian_context.config.get("empty_note_threshold", 10)
    )

    handle_command_action(items=empty_notes, delete=delete)


def register_command(cli: click.Group) -> None:
    """Register the empty notes command to the CLI group."""
    cli.add_command(empty_notes_command, name="empty-notes")
