"""Data management command for PyObsidian."""
import os
import shutil
from datetime import datetime

import click

from ..core import obsidian_context
from ..ui_handler import display_success, display_error
from .base_command import BaseCommand


@click.command(cls=BaseCommand, name="create-backup")
def create_backup() -> None:
    """Create a backup of the vault."""
    backup_path = obsidian_context.vault.create_backup()
    click.echo(f"Backup created at: {backup_path}")


@click.command(cls=BaseCommand, name="vault-stats")
def vault_stats() -> None:
    """Display vault statistics."""
    vault = obsidian_context.vault
    notes = vault.get_all_notes()
    
    total_notes = len(notes)
    total_words = sum(note.word_count for note in notes)
    total_links = sum(len(note.links) for note in notes)
    
    all_tags = set()
    for note in notes:
        all_tags.update(note.tags)
    total_tags = len(all_tags)
    
    # Use display_success for each line to ensure proper output handling
    display_success("Vault Statistics:")
    display_success(f"Total notes: {total_notes}")
    display_success(f"Total words: {total_words}")
    display_success(f"Total links: {total_links}")
    display_success(f"Total tags: {total_tags}")


@click.command(cls=BaseCommand, name="export-notes")
@click.option("--format", type=click.Choice(["markdown", "html"]), default="markdown", help="Export format")
def export_notes(format: str) -> None:
    """Export notes to markdown or HTML."""
    if format == "markdown":
        obsidian_context.vault.export_to_markdown()
        click.echo("Notes exported to markdown")
    else:
        obsidian_context.vault.export_to_html()
        click.echo("Notes exported to HTML")


def register_commands(cli: click.Group) -> None:
    """Register data management commands to the CLI group."""
    cli.add_command(create_backup)
    cli.add_command(export_notes)
    cli.add_command(vault_stats)
