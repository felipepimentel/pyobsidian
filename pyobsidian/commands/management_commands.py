import re
import click
from typing import List, Optional
from ..core import obsidian_context
from ..ui_handler import display_table, display_success

def _remove_tag(note_path: str, tag: str) -> None:
    """Remove a tag from a note."""
    note = obsidian_context.vault.notes[note_path]
    if not note:
        click.echo(f"Note '{note_path}' not found.")
        return

    # Remove tag from content
    lines = note.content.splitlines()
    modified_lines = []
    for line in lines:
        # Remove exact tag match (with word boundaries)
        line = re.sub(rf'\s*#\b{re.escape(tag)}\b', '', line)
        modified_lines.append(line)

    # Update note content
    new_content = '\n'.join(modified_lines)
    note.update_content(new_content)
    obsidian_context.vault.update_note(note_path, new_content)

def _add_tag(note_path: str, tag: str) -> None:
    """Add a tag to a note."""
    note = obsidian_context.vault.notes[note_path]
    if not note:
        click.echo(f"Note '{note_path}' not found.")
        return

    # Add tag if not already present
    if tag not in note.tags:
        note.add_tag(tag)
        obsidian_context.vault.update_note(note_path, note.content)

@click.group()
def manage() -> None:
    """Manage notes and tags."""
    pass

@manage.command()
@click.argument('note_path', type=str)
@click.argument('tag', type=str)
def add_tag(note_path: str, tag: str) -> None:
    """Add a tag to a note."""
    # Strip # if present
    tag = tag.lstrip('#')
    
    note = obsidian_context.vault.get_note(note_path)
    if not note:
        display_success(f"Note {note_path} not found.")
        return
        
    note.add_tag(tag)
    obsidian_context.vault.update_note(note_path, note.content)
    display_success(f"Added tag #{tag} to {note_path}")

@manage.command()
@click.argument('note_path', type=str)
@click.argument('tag', type=str)
def remove_tag(note_path: str, tag: str) -> None:
    """Remove a tag from a note."""
    # Strip # if present
    tag = tag.lstrip('#')
    
    note = obsidian_context.vault.get_note(note_path)
    if not note:
        display_success(f"Note {note_path} not found.")
        return
        
    note.remove_tag(tag)
    obsidian_context.vault.update_note(note_path, note.content)
    display_success(f"Removed tag #{tag} from {note_path}")

@manage.command()
def visualization() -> None:
    """Generate a visualization of the vault."""
    notes = obsidian_context.vault.get_all_notes()
    
    # Collect statistics
    total_notes = len(notes)
    total_words = sum(note.word_count for note in notes)
    total_links = sum(len(note.links) for note in notes)
    total_tags = sum(len(note.tags) for note in notes)
    
    # Display statistics
    rows = [
        ["Total Notes", str(total_notes)],
        ["Total Words", str(total_words)],
        ["Total Links", str(total_links)],
        ["Total Tags", str(total_tags)]
    ]
    
    display_table(rows, ["Metric", "Value"], title="Vault Statistics")

@manage.command()
def data() -> None:
    """Show data management information."""
    notes = obsidian_context.vault.get_all_notes()
    
    # Collect statistics about note sizes
    sizes = []
    for note in notes:
        size = len(note.content.encode('utf-8'))
        sizes.append([note.path, str(size), str(note.word_count)])
    
    # Sort by size
    sizes.sort(key=lambda x: int(x[1]), reverse=True)
    
    display_table(sizes, ["Note", "Size (bytes)", "Words"], title="Note Sizes")

@manage.command()
@click.argument('format', type=click.Choice(['json', 'markdown']))
def export(format: str) -> None:
    """Export vault data in various formats."""
    notes = obsidian_context.vault.get_all_notes()
    
    if format == 'json':
        import json
        data = {
            'notes': [
                {
                    'path': note.path,
                    'title': note.title,
                    'tags': note.tags,
                    'links': [{'target': link.target, 'alias': link.alias} for link in note.links],
                    'word_count': note.word_count
                }
                for note in notes
            ]
        }
        click.echo(json.dumps(data, indent=2))
    else:  # markdown
        for note in notes:
            click.echo(f"# {note.title}")
            click.echo(f"Path: {note.path}")
            if note.tags:
                click.echo(f"Tags: {', '.join(note.tags)}")
            if note.links:
                click.echo("Links:")
                for link in note.links:
                    click.echo(f"- {link.target}")
            click.echo(f"Word count: {note.word_count}")
            click.echo("---")

def register_commands(cli: click.Group) -> None:
    """Register management commands to the CLI group."""
    cli.add_command(manage)
    cli.add_command(add_tag)
    cli.add_command(remove_tag) 