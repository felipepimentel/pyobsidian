from typing import List

import click

from ..core import Note, ObsidianContext, Vault
from ..ui_handler import display


def get_small_notes(vault: "Vault", threshold: int) -> List[Note]:
    return [
        note
        for note in vault.get_all_notes()
        if threshold <= note.file_size < threshold * 2
    ]


def get_empty_notes(vault: "Vault", threshold: int) -> List[Note]:
    return [note for note in vault.get_all_notes() if note.file_size < threshold]


@click.command()
@click.pass_obj
def small_notes_command(ctx: ObsidianContext) -> None:
    """Identify small and empty notes."""
    small_threshold = ctx.config.get("small_note_threshold", 100)
    empty_threshold = ctx.config.get("empty_note_threshold", 10)

    empty_notes = get_empty_notes(ctx.vault, empty_threshold)
    small_notes = get_small_notes(ctx.vault, small_threshold)

    display(
        empty_notes,
        format="table",
        empty_text="No empty notes found",
        title="Empty Notes",
    )

    display(
        small_notes,
        format="table",
        empty_text="No small notes found",
        title="Small Notes",
    )


def register_command(cli: click.Group) -> None:
    cli.add_command(small_notes_command, name="small-notes")
