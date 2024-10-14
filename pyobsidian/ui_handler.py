from __future__ import annotations

from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from pyobsidian.core import Link, Note

console = Console()


def display_notes(
    notes: List["Note"], format: str = "table", title: str = "Notes"
) -> None:
    """
    Display a list of notes in the specified format.

    Args:
        notes (List[Note]): List of Note objects to display.
        format (str): Format to display the notes in ("table" or "tree").
        title (str): Title for the display.
    """
    if format == "table":
        table = Table(title=title)
        table.add_column("Filename", style="cyan")
        table.add_column("Size (bytes)", justify="right", style="magenta")

        for note in notes:
            table.add_row(note.filename, str(note.file_size))

        console.print(table)
    elif format == "tree":
        tree = Tree(title)
        for note in notes:
            tree.add(f"{note.filename} ({note.file_size} bytes)")
        console.print(tree)
    else:
        display_error(f"Unknown format: {format}")


def display_note_content(note: Note) -> None:
    """
    Display the content of a note in a rich panel with syntax highlighting.

    Args:
        note (Note): Note object to display.
    """
    syntax = Syntax(note.content, "markdown", theme="monokai", line_numbers=True)
    panel = Panel(syntax, title=note.title, expand=False)
    console.print(panel)


def display_links(links: List[Link]) -> None:
    """
    Display a list of links in a rich tree format.

    Args:
        links (List[Link]): List of Link objects to display.
    """
    tree = Tree("Links")
    for link in links:
        link_text = Text(f"{link.target}")
        if link.alias:
            link_text.append(f" (alias: {link.alias})", style="italic")
        tree.add(link_text)

    console.print(tree)


def display_error(message: str) -> None:
    """
    Display an error message in a rich format.

    Args:
        message (str): Error message to display.
    """
    console.print(f"[bold red]Error:[/bold red] {message}")


def display_success(message: str) -> None:
    """
    Display a success message in a rich format.

    Args:
        message (str): Success message to display.
    """
    console.print(f"[bold green]Success:[/bold green] {message}")


def prompt_input(prompt: str) -> str:
    """
    Prompt the user for input using rich's input method.

    Args:
        prompt (str): Prompt message for the user.

    Returns:
        str: User's input.
    """
    return console.input(f"[bold blue]{prompt}:[/bold blue] ")


def confirm_action(prompt: str) -> bool:
    """
    Prompt the user for confirmation using rich's input method.

    Args:
        prompt (str): Confirmation prompt for the user.

    Returns:
        bool: True if the user confirms, False otherwise.
    """
    response = console.input(f"[bold yellow]{prompt} (y/n):[/bold yellow] ").lower()
    return response.startswith("y")


def display_broken_links(broken_links: Dict[str, List[Link]]) -> None:
    """
    Display broken links in a tree format.

    Args:
        broken_links (Dict[str, List[Link]]): Dictionary of broken links by file.
    """
    tree = Tree("Broken Links")
    for file, links in broken_links.items():
        file_node = tree.add(file)
        for link in links:
            file_node.add(f"[red]{link.target}[/red]")

    console.print(tree)
    display_error(f"Found {len(broken_links)} notes with broken links")


def display(
    items: List[Any],
    format: str = "table",
    empty_text: str = "No items to display",
    title: Optional[str] = None,
    **kwargs,
) -> None:
    """
    Display a list of items in the specified format.

    Args:
        items (List[Any]): List of items to display.
        format (str): Format to display the items in ("table", "tree", or "links").
        empty_text (str): Text to display when the list is empty.
        title (Optional[str]): Title for the display.
        **kwargs: Additional keyword arguments for specific formats.
    """
    if not items:
        console.print(f"[green]{empty_text}[/green]")
        return

    if format == "table":
        _display_table(items, title, **kwargs)
    elif format == "tree":
        _display_tree(items, title, **kwargs)
    elif format == "links":
        _display_links(items, title, **kwargs)
    else:
        console.print(f"[red]Unknown format: {format}[/red]")


def _display_table(items: List[Any], title: Optional[str], **kwargs) -> None:
    table = Table(title=title)
    columns = kwargs.get("columns", ["Filename", "Size (bytes)"])
    for column in columns:
        table.add_column(column, style="cyan")

    for item in items:
        if isinstance(item, Note):
            table.add_row(item.filename, str(item.file_size))
        else:
            table.add_row(str(item))

    console.print(table)


def _display_tree(items: List[Any], title: Optional[str], **kwargs) -> None:
    tree = Tree(title or "Items")
    for item in items:
        if isinstance(item, Note):
            tree.add(f"{item.filename} ({item.file_size} bytes)")
        else:
            tree.add(str(item))
    console.print(tree)


def _display_links(
    items: Dict[str, List[Link]], title: Optional[str], **kwargs
) -> None:
    tree = Tree(title or "Links")
    for file, links in items.items():
        file_node = tree.add(file)
        for link in links:
            file_node.add(f"[red]{link.target}[/red]")

    console.print(tree)
    console.print(f"[red]Found {len(items)} items with links[/red]")
