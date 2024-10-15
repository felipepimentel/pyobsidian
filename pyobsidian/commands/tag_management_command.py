from typing import Dict, Set

import click

from ..core import FileOperationError, obsidian_context
from ..ui_handler import (
    display_error,
    display_standardized_tags,
    display_success,
    display_unused_tags,
)


@click.group()
def tag_management() -> None:
    """Commands for tag management and optimization."""
    pass


@tag_management.command()
def clean_unused_tags() -> None:
    """Identify and remove tags that are not used in any note."""
    vault = obsidian_context.vault
    all_tags: Set[str] = set()
    used_tags: Set[str] = set()

    for note in vault.get_all_notes():
        all_tags.update(note.tags)
        used_tags.update(note.tags)

    unused_tags = list(all_tags - used_tags)
    display_unused_tags(unused_tags)


@tag_management.command()
@click.option("--dry-run", is_flag=True, help="Show changes without applying them.")
def standardize_tags(dry_run: bool) -> None:
    """Correct inconsistencies in tag nomenclature and ensure they follow a standard format."""
    vault = obsidian_context.vault
    all_tags: Set[str] = set()
    standardized_tags: Dict[str, str] = {}

    # Primeiro, colete todas as tags e crie o mapeamento de padronização
    for note in vault.get_all_notes():
        all_tags.update(note.tags)

    for tag in all_tags:
        standardized = tag.lower().replace(" ", "_")
        if tag != standardized:
            standardized_tags[tag] = standardized

    if not dry_run:
        updated_count = 0
        error_count = 0
        skipped_count = 0
        for note in vault.get_all_notes():
            updated = False
            new_tags = set()
            for tag in note.tags:
                if tag in standardized_tags:
                    new_tags.add(standardized_tags[tag])
                    updated = True
                else:
                    new_tags.add(tag)
            if updated:
                # Update the note's content with new tags
                new_content = note.content
                for old_tag, new_tag in standardized_tags.items():
                    new_content = new_content.replace(f"#{old_tag}", f"#{new_tag}")

                note.tags = new_tags
                try:
                    vault.update_note(note, new_content)
                    updated_count += 1
                except FileOperationError as e:
                    if "Note not found" in str(e):
                        skipped_count += 1
                    else:
                        display_error(
                            f"Failed to update note {note.filename}: {str(e)}"
                        )
                        error_count += 1

        display_success(
            f"Updated {updated_count} notes. Skipped {skipped_count} notes. Encountered {error_count} errors."
        )

    display_standardized_tags(standardized_tags, dry_run)


def register_command(cli: click.Group) -> None:
    """Register the tag management commands to the CLI group."""
    cli.add_command(tag_management)
