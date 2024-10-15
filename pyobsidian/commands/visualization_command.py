import click

from ..core import obsidian_context
from ..ui_handler import (
    display_link_density,
    display_note_relationships,
    display_vault_growth,
)


@click.group()
def visualization() -> None:
    """Commands for visualization and reporting."""
    pass


@visualization.command()
def note_relationships() -> None:
    """Generate a graphical visualization of links between notes."""
    vault = obsidian_context.vault
    notes = vault.get_all_notes()
    relationships = []
    for note in notes:
        for link in note.links:
            relationships.append((note.title, link.target))
    display_note_relationships(relationships)


@visualization.command()
def vault_growth() -> None:
    """Generate reports on Vault growth over time."""
    vault = obsidian_context.vault
    notes = vault.get_all_notes()
    growth_data = {"created": {}, "modified": {}}

    for note in notes:
        if note.created_at:
            created_date = note.created_at.strftime("%Y-%m-%d")
            growth_data["created"][created_date] = (
                growth_data["created"].get(created_date, 0) + 1
            )

        if note.updated_at:
            modified_date = note.updated_at.strftime("%Y-%m-%d")
            growth_data["modified"][modified_date] = (
                growth_data["modified"].get(modified_date, 0) + 1
            )

    display_vault_growth(growth_data)


@visualization.command()
def link_density() -> None:
    """Generate reports showing which notes have the highest link density and which are isolated."""
    vault = obsidian_context.vault
    notes = vault.get_all_notes()
    link_data = {}
    for note in notes:
        link_data[note.title] = len(note.links)

    display_link_density(link_data)


def register_command(cli: click.Group) -> None:
    """Register the visualization commands to the CLI group."""
    cli.add_command(visualization)
