from datetime import datetime
from typing import List, Optional

import click

from ..core import Note, Vault, obsidian_context
from ..ui_handler import display_saved_filters, handle_command_action


def search_notes(
    vault: "Vault",
    keyword: str,
    tags: List[str] = None,
    created_after: Optional[datetime] = None,
    modified_after: Optional[datetime] = None,
    min_links: Optional[int] = None,
) -> List[Note]:
    """Search for notes based on various criteria."""
    matching_notes = []
    for note in vault.get_all_notes():
        if keyword.lower() not in note.content.lower():
            continue
        if tags and not set(tags).issubset(note.tags):
            continue
        if created_after and note.created_at < created_after:
            continue
        if modified_after and note.updated_at < modified_after:
            continue
        if min_links is not None and len(note.links) < min_links:
            continue
        matching_notes.append(note)
    return matching_notes


@click.group()
def search() -> None:
    """Commands for searching and filtering notes."""
    pass


@search.command()
@click.argument("keyword", type=str)
@click.option("--tags", multiple=True, help="Filter by tags")
@click.option("--created-after", type=click.DateTime(), help="Filter by creation date")
@click.option(
    "--modified-after", type=click.DateTime(), help="Filter by modification date"
)
@click.option("--min-links", type=int, help="Filter by minimum number of links")
@click.option("--delete", is_flag=True, help="Delete the identified notes")
def search_command(
    keyword: str,
    tags: List[str],
    created_after: click.DateTime,
    modified_after: click.DateTime,
    min_links: int,
    delete: bool,
) -> None:
    """Search for notes containing a specific word and apply advanced filters."""
    matching_notes = search_notes(
        obsidian_context.vault, keyword, tags, created_after, modified_after, min_links
    )
    handle_command_action(items=matching_notes, delete=delete)


@search.command()
@click.argument("name")
@click.argument("query")
def save_filter(name: str, query: str) -> None:
    """Save a custom filter for future use."""
    saved_filters = obsidian_context.get_saved_filters()
    saved_filters[name] = query
    obsidian_context.save_filters(saved_filters)
    display_saved_filters(saved_filters)


@search.command()
def list_saved_filters() -> None:
    """List all saved custom filters."""
    saved_filters = obsidian_context.get_saved_filters()
    display_saved_filters(saved_filters)


def register_command(cli: click.Group) -> None:
    """Register the search commands to the CLI group."""
    cli.add_command(search)
