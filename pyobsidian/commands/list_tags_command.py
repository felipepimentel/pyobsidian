from collections import Counter
from typing import List, Tuple

import click

from ..core import Vault, obsidian_context
from ..ui_handler import handle_command_action


def get_tag_counts(vault: "Vault") -> List[Tuple[str, int]]:
    """
    Get a list of tuples containing tags and their counts across all notes.

    Args:
        vault (Vault): The Obsidian vault to search for tags.

    Returns:
        List[Tuple[str, int]]: A list of tuples, each containing a tag and its count,
                               sorted in descending order by count.
    """
    tag_counter = Counter()
    for note in vault.get_all_notes():
        tag_counter.update(note.tags)
    return sorted(tag_counter.items(), key=lambda x: x[1], reverse=True)


@click.command()
@click.option("--min-count", default=1, help="Minimum count to display a tag")
def list_tags_command(min_count: int) -> None:
    """
    List all tags used in the vault with their counts.

    Args:
        min_count (int): The minimum count threshold for displaying a tag.
    """
    tag_counts = get_tag_counts(obsidian_context.vault)
    filtered_tags = [
        f"#{tag}: {count}" for tag, count in tag_counts if count >= min_count
    ]

    handle_command_action(
        items=filtered_tags,
        item_type="tags",
        display_format="list",
        empty_text="No tags found matching the criteria",
        title="Tags in the Vault",
    )


def register_command(cli: click.Group) -> None:
    """Register the list tags command to the CLI group."""
    cli.add_command(list_tags_command, name="list-tags")
