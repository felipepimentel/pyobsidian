"""UI handler for PyObsidian."""
from typing import Dict, List, Optional, Tuple, Union
import sys
import os

import click
from rich.console import Console
from rich.table import Table

from .core import Note, Link

# Create a console that writes to stderr for rich output
# In test environments, we want to suppress output
console = Console(file=sys.stderr if not os.getenv("PYTEST_CURRENT_TEST") else None)

def _echo(message: str, err: bool = True) -> None:
    """Echo a message, properly handling bytes vs strings."""
    if isinstance(message, str):
        message = message.encode('utf-8')
    click.echo(message, err=err)

def display_table(rows: List[List[str]], headers: List[str], title: Optional[str] = None) -> None:
    """Display data in a table format."""
    # Create table
    table = Table(show_header=True, header_style="bold magenta")
    
    # Add columns
    for header in headers:
        table.add_column(header)
    
    # Add rows if any
    if rows:
        for row in rows:
            # Convert all values to strings
            str_row = [str(value) for value in row]
            table.add_row(*str_row)
    
    # Create console and print
    console = Console()
    if title:
        console.print(f"\n[bold]{title}[/bold]")
    console.print(table)


def display_notes(notes: List[Note], title: str = "Notes") -> None:
    """Display a list of notes in a table format."""
    rows = []
    for note in notes:
        rows.append([
            str(note.path),
            note.title or "(No title)",
            str(note.word_count),
            ", ".join(f"#{tag}" for tag in sorted(note.tags)) if note.tags else ""
        ])
    display_table(rows, ["Path", "Title", "Words", "Tags"], title=title)


def display_empty_notes(notes: List[Note]) -> None:
    """Display empty notes."""
    display_notes(notes, "Empty Notes")


def display_small_notes(notes: List[Note]) -> None:
    """Display small notes in a table format."""
    if not notes:
        _echo("No small notes found.")
        return

    # Create table headers
    headers = ["Path", "Title", "Words", "Tags"]
    rows = []

    # Create table rows
    for note in notes:
        rows.append([
            note.path,
            note.title or "(No title)",
            str(note.word_count),
            ", ".join(f"#{tag}" for tag in note.tags) if note.tags else ""
        ])

    # Display table
    display_table(rows, headers, "Small Notes")


def display_broken_links(notes_with_broken_links: List[Tuple[Note, List[Link]]]) -> None:
    """Display notes with broken links."""
    if not notes_with_broken_links:
        _echo("No broken links found.")
        return

    headers = ["Note Path", "Title", "Broken Link Target", "Link Alias"]
    rows = []
    for note, broken_links in notes_with_broken_links:
        for link in broken_links:
            rows.append([
                note.path,
                note.title,
                link.target,
                link.alias or ""
            ])
    display_table(rows, headers, "Broken Links")


def display_orphan_notes(notes: List[Note]) -> None:
    """Display orphaned notes."""
    display_notes(notes, "Orphaned Notes")


def display_tags(tag_counts: Dict[str, int]) -> None:
    """Display tag counts in a table format."""
    rows = []
    for tag, count in sorted(tag_counts.items()):
        rows.append([f"#{tag}", str(count)])
    display_table(rows, ["Tag", "Count"], title="Tags")


def display_notes_by_tag(notes: List[Note], tag: str) -> None:
    """Display notes that have a specific tag."""
    rows = []
    for note in notes:
        rows.append([
            str(note.path),
            note.title or "(No title)",
            str(note.word_count),
            ", ".join(f"#{t}" for t in sorted(note.tags)) if note.tags else ""
        ])
    display_table(rows, ["Path", "Title", "Words", "Tags"], title=f"Notes with tag #{tag}")


def display_search_results(notes: List[Note]) -> None:
    """Display search results."""
    display_notes(notes, "Search Results")


def display_success(message: str) -> None:
    """Display a success message."""
    _echo(message)


def display_error(message: str) -> None:
    """Display an error message."""
    _echo(f"Error: {message}")


def display_folders(folders: List[str], title: str = "Folders") -> None:
    """Display a list of folders in a table format."""
    if not folders:
        _echo("No empty folders found")
        return
    
    headers = [title]
    rows = [[folder] for folder in folders]
    display_table(rows, headers)


def display_tag_added(note_path: str, tag: str) -> None:
    """Display message when a tag is added."""
    _echo(f"Added tag '#{tag}' to note '{note_path}'")


def display_tag_removed(note_path: str, tag: str) -> None:
    """Display message when a tag is removed."""
    _echo(f"Removed tag '#{tag}' from note '{note_path}'")


def display_note_not_found(note_path: str) -> None:
    """Display message when a note is not found."""
    _echo(f"Error: Note '{note_path}' not found.")


def display_note_relationships(relationships: List[Tuple[str, str]]) -> None:
    """Display note relationships."""
    if not relationships:
        _echo("No relationships found between notes.")
        return

    headers = ["Source Note", "Target Note"]
    rows = [[source, target] for source, target in relationships]
    display_table(rows, headers, "Graph visualization")


def display_tag_usage(tag_counts: Dict[str, int]) -> None:
    """Display tag usage statistics."""
    if not tag_counts:
        _echo("No tags found in the vault.")
        return

    headers = ["Tag", "Usage Count"]
    rows = [[f"#{tag}", str(count)] for tag, count in sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))]
    display_table(rows, headers, "Tag cloud visualization")


def display_export_result(result: str) -> None:
    """Display export operation result."""
    if result:
        display_success(result)
    else:
        display_error("Export operation failed")


def display_word_cloud(word_stats: List[Tuple[str, int, float]], message: str = None) -> None:
    """Display word cloud statistics in a table format."""
    if not word_stats and message:
        display_table([], ["Word", "Count", "Percentage"], title=message)
        return
    
    rows = [
        [word, str(count), f"{percentage:.1f}%"]
        for word, count, percentage in word_stats
    ]
    
    display_table(rows, ["Word", "Count", "Percentage"], 
                 title="Word Cloud (min length: 3, min count: 2)")
