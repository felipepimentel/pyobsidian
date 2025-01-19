import click
from .. import obsidian_context
from ..ui_handler import display_empty_notes, display_small_notes

@click.command()
def empty_notes() -> None:
    """Find notes with no content."""
    notes = obsidian_context.vault.get_empty_notes()
    display_empty_notes(notes)

@click.command()
@click.option("--min-words", default=50, help="Minimum word count threshold")
def small_notes(min_words: int) -> None:
    """Find notes with fewer than min_words words."""
    notes = [note for note in obsidian_context.vault.notes.values() 
            if 0 < note.word_count < min_words]
    display_small_notes(notes, min_words)

def register_command(cli: click.Group) -> None:
    """Register the content analysis commands to the CLI group."""
    cli.add_command(empty_notes)
    cli.add_command(small_notes) 