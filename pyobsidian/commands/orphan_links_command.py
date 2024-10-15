from typing import List, Tuple

import click

from ..core import obsidian_context
from ..ui_handler import display_orphan_links


@click.command()
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Exibir informações detalhadas sobre os links órfãos.",
)
def orphan_links(verbose: bool) -> None:
    """Detecta links órfãos no vault do Obsidian."""
    vault = obsidian_context.vault
    orphans = find_orphan_links(vault)
    display_orphan_links(orphans, verbose)


def find_orphan_links(vault) -> List[Tuple[str, List[str]]]:
    """
    Encontra links órfãos no vault.

    Args:
        vault: O objeto Vault do Obsidian.

    Returns:
        Uma lista de tuplas contendo o nome da nota e seus links órfãos.
    """
    all_notes = vault.get_all_notes()
    note_names = {note.name for note in all_notes}
    orphans = []

    for note in all_notes:
        orphan_links = []
        for link in note.links:
            if link.target not in note_names:
                orphan_links.append(link.target)
        if orphan_links:
            orphans.append((note.name, orphan_links))

    return orphans


def register_command(cli: click.Group) -> None:
    """Registra o comando orphan-links no grupo CLI."""
    cli.add_command(orphan_links, name="orphan-links")
