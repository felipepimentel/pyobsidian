import os
from typing import List

import click

from ..core import Vault, obsidian_context
from ..ui_handler import handle_command_action


def get_empty_folders(vault: "Vault") -> List[str]:
    """Find empty folders in the vault."""
    empty_folders = []
    for root, dirs, files in os.walk(vault.config.vault_path):
        if not dirs and not files:
            empty_folders.append(root)
    return empty_folders


@click.command()
@click.option("--delete", is_flag=True, help="Delete the identified empty folders")
def empty_folders_command(delete: bool) -> None:
    """Identify empty folders in the vault."""
    empty_folders = get_empty_folders(obsidian_context.vault)

    handle_command_action(items=empty_folders, delete=delete)


def register_command(cli: click.Group) -> None:
    """Register the empty folders command to the CLI group."""
    cli.add_command(empty_folders_command, name="empty-folders")
