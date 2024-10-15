from __future__ import annotations

import os
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from pyobsidian.core import Link, Note, obsidian_context

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
    items: Union[List[Any], Dict[str, List[Note]]],
    format: str = "table",
    empty_text: str = "No items to display",
    title: Optional[str] = None,
    filter_tag: Optional[str] = None,
    **kwargs,
) -> None:
    """
    Display a list of items or a dictionary of tags and notes in the specified format.

    Args:
        items (Union[List[Any], Dict[str, List[Note]]]): List of items or dictionary of tags and notes to display.
        format (str): Format to display the items in ("table", "tree", "links", "tags_and_notes", or "list").
        empty_text (str): Text to display when the list is empty.
        title (Optional[str]): Title for the display.
        filter_tag (Optional[str]): Specific tag to filter notes (for tags_and_notes format).
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
    elif format == "tags_and_notes":
        _display_tags_and_notes(items, title, filter_tag, **kwargs)
    elif format == "list":
        _display_list(items, title, **kwargs)
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


def _display_tags_and_notes(
    items: Dict[str, List[Note]],
    title: Optional[str],
    filter_tag: Optional[str] = None,
    **kwargs,
) -> None:
    if filter_tag:
        notes = items.get(filter_tag, [])
        if notes:
            table = Table(title=f"Notes with tag: #{filter_tag}")
            table.add_column("Title", style="cyan")
            table.add_column("Path", style="magenta")
            for note in notes:
                table.add_row(note.title, note.path)
            console.print(table)
        else:
            console.print(f"[yellow]No notes found with tag: #{filter_tag}[/yellow]")
    else:
        tree = Tree(title or "Tags and Notes")
        for tag, notes in items.items():
            tag_node = tree.add(f"[bold blue]#{tag}[/bold blue]")
            for note in notes:
                tag_node.add(f"[cyan]{note.title}[/cyan] ({note.path})")
        console.print(tree)


def _display_list(items: List[Any], title: Optional[str], **kwargs) -> None:
    if title:
        console.print(f"[bold]{title}[/bold]")

    for item in items:
        console.print(item)


def handle_bulk_action(
    items: List[Any], item_type: str, action: Callable[[List[Any]], None]
) -> None:
    """
    Handle bulk actions on a list of items.

    Args:
        items (List[Any]): The list of items to process.
        item_type (str): The type of items being processed.
        action (Callable[[List[Any]], None]): The action to perform on the items.
    """
    if not items:
        display_success(f"No {item_type} found.")
        return

    display(items, format="table", title=f"{item_type.capitalize()} to process")
    if confirm_action(f"Do you want to process these {item_type}?"):
        action(items)
        display_success(f"Processed {len(items)} {item_type}.")
    else:
        display_error("Action cancelled.")


def handle_command_action(
    items: Union[List[Union[Note, str]], Dict[str, List[Note]]],
    item_type: Optional[str] = None,
    delete: bool = False,
    display_format: str = "table",
    empty_text: str = "No items found",
    title: Optional[str] = None,
    filter_tag: Optional[str] = None,
) -> None:
    """
    Handle command actions for displaying or deleting items.
    """
    if not items:
        display_success(empty_text)
        return

    if item_type == "notes_by_tag":
        display(
            items,
            format=display_format,
            empty_text=empty_text,
            title=title,
            filter_tag=filter_tag,
        )
    else:
        if item_type is None and items:
            item_type = "notes" if isinstance(items[0], Note) else "folders"

        display(
            items,
            format=display_format,
            empty_text=empty_text,
            title=title or f"{item_type.capitalize()}",
        )

    if delete and isinstance(items, list):
        if click.confirm(f"Do you want to delete these {item_type}?"):
            for item in items:
                if isinstance(item, Note):
                    obsidian_context.vault.delete_note(item)
                else:
                    try:
                        os.rmdir(item)
                    except OSError as e:
                        display_error(f"Error deleting folder {item}: {str(e)}")
            display_success(f"{len(items)} {item_type} deleted successfully.")
        else:
            display_success("Deletion cancelled.")


def display_orphan_links(orphans: List[Tuple[str, List[str]]], verbose: bool) -> None:
    """
    Exibe os links órfãos encontrados no vault.

    Args:
        orphans: Uma lista de tuplas contendo o nome da nota e seus links órfãos.
        verbose: Se True, exibe informações detalhadas sobre os links órfãos.
    """
    if not orphans:
        console.print("[green]Nenhum link órfão encontrado no vault.[/green]")
        return

    console.print(f"[bold]Encontrados {len(orphans)} notas com links órfãos:[/bold]")

    tree = Tree("Links Órfãos")
    for note_name, orphan_links in orphans:
        note_node = tree.add(f"[cyan]{note_name}[/cyan]")
        for link in orphan_links:
            if verbose:
                note_node.add(f"[red]{link}[/red]")
            else:
                truncated_link = f"{link[:30]}..." if len(link) > 30 else link
                note_node.add(f"[red]{truncated_link}[/red]")

    console.print(tree)

    if not verbose:
        console.print(
            "\n[yellow]Use a opção --verbose para ver os links completos.[/yellow]"
        )


def display_unused_tags(unused_tags: List[str]) -> None:
    click.echo("Unused tags:")
    for tag in unused_tags:
        click.echo(f"- {tag}")


def display_standardized_tags(standardized_tags: Dict[str, str], dry_run: bool) -> None:
    click.echo("Standardized tags:")
    for old_tag, new_tag in standardized_tags.items():
        click.echo(f"- {old_tag} -> {new_tag}")
    if dry_run:
        click.echo("This was a dry run. No changes were applied.")


def display_note_relationships(relationships: List[Tuple[str, str]]) -> None:
    click.echo("Note relationships:")
    for source, target in relationships:
        click.echo(f"- {source} -> {target}")


def display_vault_growth(growth_data: Dict[str, Dict[str, int]]) -> None:
    click.echo("Vault growth:")
    for action, data in growth_data.items():
        click.echo(f"{action.capitalize()}:")
        for date, count in data.items():
            click.echo(f"- {date}: {count}")


def display_link_density(link_data: Dict[str, int]) -> None:
    click.echo("Link density:")
    sorted_data = sorted(link_data.items(), key=lambda x: x[1], reverse=True)
    for note, links in sorted_data:
        click.echo(f"- {note}: {links} links")


def display_sensitive_data(
    sensitive_notes: Dict[str, Dict[str, List[str]]], verbose: bool
) -> None:
    if not sensitive_notes:
        console.print("[green]No sensitive data detected in any notes.[/green]")
        return

    table = Table(title="Notes with Potentially Sensitive Data")
    table.add_column("Note Title", style="cyan")
    table.add_column("Sensitive Data Type", style="magenta")
    table.add_column("Occurrences", justify="right", style="green")

    if verbose:
        table.add_column("Matched Data", style="yellow")

    for note_title, data_types in sensitive_notes.items():
        for data_type, matches in data_types.items():
            if verbose:
                for match in matches:
                    table.add_row(note_title, data_type, str(len(matches)), match)
            else:
                table.add_row(note_title, data_type, str(len(matches)))

    console.print(table)

    total_notes = len(sensitive_notes)
    total_matches = sum(
        len(matches)
        for data_types in sensitive_notes.values()
        for matches in data_types.values()
    )
    console.print("\n[bold]Summary:[/bold]")
    console.print(f"- Total notes with sensitive data: {total_notes}")
    console.print(f"- Total sensitive data occurrences: {total_matches}")

    if not verbose:
        console.print("\n[yellow]Use --verbose flag to see detailed matches.[/yellow]")


def display_export_result(result: str) -> None:
    click.echo(result)


def display_filtered_notes(notes: List[object]) -> None:
    click.echo("Filtered notes:")
    for note in notes:
        click.echo(f"- {note.title}")


def display_saved_filters(filters: Dict[str, str]) -> None:
    click.echo("Saved filters:")
    for name, query in filters.items():
        click.echo(f"- {name}: {query}")
