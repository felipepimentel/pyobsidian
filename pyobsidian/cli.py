# pyobsidian/cli.py

import click

from .commands import register_all_commands
from .core import ObsidianContext


@click.group()
@click.option("--config", default="config.yaml", help="Path to config file")
@click.pass_context
def cli(ctx: click.Context, config: str) -> None:
    """Obsidian management CLI."""
    ctx.obj = ObsidianContext(config)


register_all_commands(cli)

if __name__ == "__main__":
    cli()
