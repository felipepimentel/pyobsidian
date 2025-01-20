import click
from typing import List
from ..core import obsidian_context
from ..ui_handler import display_table, display_success
from rich.table import Table
from rich.console import Console

@click.command()
def empty_notes() -> None:
    """Find empty notes in the vault."""
    notes = obsidian_context.vault.get_empty_notes()
    
    if not notes:
        click.echo("No empty notes found.")
        return
    
    rows = []
    for note in notes:
        rows.append([note.path, note.title, str(note.word_count), ", ".join(note.tags)])
    
    display_table(rows, ["Path", "Title", "Words", "Tags"], title="Empty Notes")

@click.command()
def small_notes() -> None:
    """Find notes with fewer than 5 words."""
    notes = obsidian_context.vault.get_all_notes()
    small = []
    
    for note in notes:
        if note.word_count < 5:
            small.append(note)
    
    # Sort by word count and path
    small.sort(key=lambda x: (x.word_count, x.path))
    
    # Display results
    rows = []
    for note in small:
        rows.append([
            str(note.path),
            note.title or "(No title)",
            str(note.word_count),
            ", ".join(f"#{tag}" for tag in sorted(note.tags)) if note.tags else ""
        ])
    
    display_table(rows, ["Path", "Title", "Words", "Tags"], title="Small Notes")

@click.command()
def empty_folders() -> None:
    """Find empty folders in the vault."""
    folders = obsidian_context.vault.get_empty_folders()
    
    if not folders:
        click.echo("No empty folders found.")
        return
    
    rows = [[folder] for folder in sorted(folders)]
    display_table(rows, ["Path"], title="Empty Folders")

def register_commands(cli: click.Group) -> None:
    """Register content analysis commands to the CLI group."""
    cli.add_command(empty_notes, name="empty-notes")
    cli.add_command(small_notes, name="small-notes")
    cli.add_command(empty_folders, name="empty-folders") 