"""Tag management command."""
import click
import re

from ..core import obsidian_context
from ..ui_handler import display_success, display_error
from .base_command import BaseCommand


@click.command(cls=BaseCommand, name="add-tag")
@click.argument("note_path")
@click.argument("tag")
def add_tag(note_path: str, tag: str) -> None:
    """Add a tag to a note."""
    try:
        note = obsidian_context.vault.get_note(note_path)
        if note is None:
            display_error(f"Note '{note_path}' not found.")
            return

        note.add_tag(tag)
        obsidian_context.vault.update_note(note_path, note.content)
        display_success(f"Added tag '#{tag}' to note '{note_path}'")
    except Exception as e:
        display_error(f"Failed to add tag: {str(e)}")


@click.command(cls=BaseCommand, name="remove-tag")
@click.argument("note_path")
@click.argument("tag")
def remove_tag(note_path: str, tag: str) -> None:
    """Remove a tag from a note."""
    try:
        note = obsidian_context.vault.get_note(note_path)
        if note is None:
            display_error(f"Note '{note_path}' not found.")
            return

        note.remove_tag(tag)
        obsidian_context.vault.update_note(note_path, note.content)
        display_success(f"Removed tag '#{tag}' from note '{note_path}'")
    except Exception as e:
        display_error(f"Failed to remove tag: {str(e)}")


@click.command(cls=BaseCommand)
@click.argument("old_tag")
@click.argument("new_tag")
def replace_tag(old_tag: str, new_tag: str) -> None:
    """Replace all occurrences of OLD_TAG with NEW_TAG in all notes."""
    try:
        # Strip # from tags if present
        old_tag = old_tag.lstrip('#')
        new_tag = new_tag.lstrip('#')
        
        notes_updated = 0
        for note in obsidian_context.vault.notes.values():
            # Check if the note contains the old tag
            if old_tag in [tag.lstrip('#') for tag in note.tags]:
                # Replace the tag in the content
                content = note.content
                # Use regex to ensure we only replace exact tag matches
                content = re.sub(f'#({old_tag})(?![\\w-])', f'#{new_tag}', content)
                
                # Update the note content and force reload of tags
                obsidian_context.vault.update_note(note.path, content)
                note.update_content(content)
                # Ensure the note object is updated in the vault
                obsidian_context.vault.notes[note.path] = note
                notes_updated += 1
        
        if notes_updated > 0:
            display_success(f"Replaced tag #{old_tag} with #{new_tag} in {notes_updated} notes.")
        else:
            display_success(f"No notes found with tag #{old_tag}.")
    except Exception as e:
        display_error(f"Failed to replace tag: {str(e)}")


def register_command(cli: click.Group) -> None:
    """Register the tag management commands to the CLI group."""
    cli.add_command(add_tag)
    cli.add_command(remove_tag)
    cli.add_command(replace_tag)
