"""Empty folders command for PyObsidian."""
import os
from typing import List

import click

from ..core import obsidian_context
from ..ui_handler import display_folders
from .base_command import BaseCommand


def get_empty_folders(vault_path: str) -> List[str]:
    """Get all empty folders in the vault."""
    empty_folders = []
    for root, dirs, files in os.walk(vault_path):
        # Filter out hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        
        # Check if directory is empty (no files and no subdirectories)
        if not dirs and not files:
            empty_folders.append(os.path.relpath(root, vault_path))
    
    return empty_folders


@click.command(cls=BaseCommand)
def empty_folders() -> None:
    """List all empty folders in the vault."""
    folders = obsidian_context.vault.get_empty_folders()
    display_folders(folders)


def register_command(cli: click.Group) -> None:
    """Register the empty-folders command to the CLI group."""
    cli.add_command(empty_folders)
