"""Search commands for PyObsidian."""
import click
from collections import Counter
from typing import List
from ..core import obsidian_context
from ..ui_handler import display_table, display_success, display_tags, display_notes, display_notes_by_tag
from rich.table import Table
from rich.console import Console

@click.command()
def list_tags() -> None:
    """List all tags in the vault."""
    tag_counts = obsidian_context.vault.get_all_tags()
    if not tag_counts:
        display_success("No tags found.")
        return
    
    rows = [
        [f"#{tag}", str(count)]
        for tag, count in sorted(tag_counts.items())
    ]
    
    display_table(rows, ["Tag", "Count"], title="Tags")

@click.command()
@click.argument('tag')
def notes_by_tag(tag: str) -> None:
    """List all notes with a specific tag."""
    # Strip # from tag if present
    tag = tag.lstrip('#')
    
    notes = obsidian_context.vault.get_notes_by_tag(tag)
    if not notes:
        display_success(f"No notes found with tag #{tag}.")
        return
    
    rows = []
    for note in notes:
        rows.append([
            str(note.path),
            note.title or "(No title)",
            ", ".join(f"#{t}" for t in sorted(note.tags)) if note.tags else ""
        ])
    
    display_table(rows, ["Path", "Title", "Tags"], title=f"Notes with tag #{tag}")

def register_commands(cli: click.Group) -> None:
    """Register search commands to the CLI group."""
    cli.add_command(list_tags)
    cli.add_command(notes_by_tag) 