"""Tag management command."""
import click
import re

from ..core import obsidian_context
from ..ui_handler import display_success, display_error
from .base_command import BaseCommand


@click.command()
@click.argument('note_path')
@click.argument('tag')
def add_tag(note_path: str, tag: str) -> None:
    """Add a tag to a note."""
    note = obsidian_context.vault.get_note(note_path)
    if not note:
        display_error(f"Note {note_path} not found.")
        return
    
    try:
        # Ensure tag starts with #
        if not tag.startswith('#'):
            tag = f'#{tag}'
        
        # Add tag to content
        if tag not in note.tags:
            if note.content.strip():
                # Add tag at the end of the first line
                lines = note.content.split('\n')
                lines[0] = lines[0].strip() + f' {tag}'
                note.content = '\n'.join(lines)
            else:
                # If content is empty, just add the tag
                note.content = tag
            
            # Save the note
            note.save()
            display_success(f"Added tag {tag} to {note_path}")
        else:
            display_error(f"Tag {tag} already exists in {note_path}")
    except ValueError as e:
        display_error(str(e))


@click.command()
@click.argument('tag')
@click.argument('note_path')
def remove_tag(tag: str, note_path: str) -> None:
    """Remove a tag from a note."""
    try:
        note = obsidian_context.vault.get_note(note_path)
        if not note:
            display_error(f"Note {note_path} not found.")
            return
        
        # Strip # from tag if present
        tag = tag.lstrip('#')
        
        note.remove_tag(tag)
        note.save()
        display_success(f"Removed tag #{tag} from {str(note.path)}")
    except ValueError as e:
        display_error(str(e))


@click.command()
@click.argument('old_tag')
@click.argument('new_tag')
@click.argument('note_path')
def replace_tag(old_tag: str, new_tag: str, note_path: str) -> None:
    """Replace a tag in a note with a new one."""
    try:
        note = obsidian_context.vault.get_note(note_path)
        if not note:
            display_error(f"Note {note_path} not found.")
            return
        
        # Strip # from tags if present
        old_tag = old_tag.lstrip('#')
        new_tag = new_tag.lstrip('#')
        
        note.remove_tag(old_tag)
        note.add_tag(new_tag)
        note.save()
        display_success(f"Replaced tag #{old_tag} with #{new_tag} in {str(note.path)}")
    except ValueError as e:
        display_error(str(e))


def register_command(cli: click.Group) -> None:
    """Register tag management commands to the CLI group."""
    cli.add_command(add_tag, name="add-tag")
    cli.add_command(remove_tag, name="remove-tag")
    cli.add_command(replace_tag, name="replace-tag")
