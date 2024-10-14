from typing import Dict, List

import click

from ..core import Link, ObsidianContext, Vault


def get_broken_links(vault: "Vault") -> Dict[str, List[Link]]:
    broken_links = {}
    for note in vault.get_all_notes():
        broken = [link for link in note.links if not vault.get_note(link.target)]
        if broken:
            broken_links[note.path] = broken
    return broken_links


@click.command()
@click.pass_obj
def broken_links_command(ctx: ObsidianContext) -> None:
    """Identify broken links in notes."""
    broken_links = get_broken_links(ctx.vault)
    click.echo(f"Found {len(broken_links)} notes with broken links")
    for file, links in broken_links.items():
        click.echo(f"\n{file}:")
        for link in links:
            click.echo(f"  - {link.target}")


def register_command(cli: click.Group) -> None:
    cli.add_command(broken_links_command, name="broken-links")
