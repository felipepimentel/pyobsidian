import click
from typing import List, Tuple
from ..core import obsidian_context
from ..ui_handler import display_table
from ..link import Link

@click.command()
@click.option('--include-empty', is_flag=True, help='Include empty notes in the results.')
def orphan_notes(include_empty: bool) -> None:
    """Find notes that no other notes link to."""
    notes = obsidian_context.vault.get_orphan_notes()
    
    if include_empty:
        empty_notes = obsidian_context.vault.get_empty_notes()
        notes.extend(note for note in empty_notes if note not in notes)
    
    if not notes:
        click.echo("No orphaned notes found.")
        return
    
    rows = []
    for note in sorted(notes):
        rows.append([note.path, note.title, str(note.word_count), ", ".join(note.tags)])
    
    display_table(rows, ["Path", "Title", "Words", "Tags"], title="Orphaned Notes")

@click.command()
def broken_links() -> None:
    """Find broken links in notes."""
    broken = obsidian_context.vault.get_broken_links()
    
    if not broken:
        click.echo("No broken links found.")
        return
    
    rows = []
    for note, links in sorted(broken, key=lambda x: x[0].path):
        for link in sorted(links, key=lambda x: x.target):
            rows.append([
                note.path,
                link.target,
                link.alias or ""
            ])
    
    display_table(rows, ["Note", "Target", "Alias"], title="Broken Links")

def register_commands(cli: click.Group) -> None:
    """Register link commands to the CLI group."""
    cli.add_command(orphan_notes, name="orphan-notes")
    cli.add_command(broken_links, name="broken-links") 