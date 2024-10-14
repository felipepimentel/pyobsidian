from typing import List

import click

from ..core import Note, ObsidianContext, Vault


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

    small_notes = get_small_notes(ctx.vault, small_threshold)
    empty_notes = get_empty_notes(ctx.vault, empty_threshold)

    click.echo(f"Small notes: {len(small_notes)}")
    click.echo(f"Empty notes: {len(empty_notes)}")


def register_command(cli: click.Group) -> None:
    cli.add_command(small_notes_command, name="small-notes")
