from typing import List

import click

from ..core import Note, Vault, obsidian_context
from ..ui_handler import handle_command_action


def get_small_notes(vault: "Vault", threshold: int) -> List[Note]:
    return [note for note in vault.get_all_notes() if note.word_count < threshold]


@click.command()
@click.option("--delete", is_flag=True, help="Delete the identified small notes")
@click.option("--threshold", default=50, help="Word count threshold for small notes")
def small_notes_command(delete: bool, threshold: int) -> None:
    """Identify small notes based on word count."""
    small_notes = get_small_notes(obsidian_context.vault, threshold)

    handle_command_action(items=small_notes, delete=delete)


def register_command(cli: click.Group) -> None:
    """Register the small notes command to the CLI group."""
    cli.add_command(small_notes_command, name="small-notes")
