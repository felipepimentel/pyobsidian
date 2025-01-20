# pyobsidian/cli.py

import importlib
from pathlib import Path
from typing import Callable

import click

from .core import ObsidianContext
from .commands import (
    empty_notes_command,
    small_notes_command,
    empty_folders_command,
    daily_stats_command,
    word_cloud_command,
    find_similar_command
)


def load_commands(cli: click.Group) -> None:
    """
    Dynamically load and register commands from the 'commands' directory.

    Args:
        cli (click.Group): The CLI group to which commands will be added.
    """
    commands_dir = Path(__file__).parent / "commands"
    for file in commands_dir.glob("*_command.py"):
        module_name = f"pyobsidian.commands.{file.stem}"
        module = importlib.import_module(module_name)
        if hasattr(module, "register_command"):
            register_func: Callable[[click.Group], None] = getattr(
                module, "register_command"
            )
            register_func(cli)


@click.group()
@click.option("--config", default="config.yaml", help="Path to config file")
@click.pass_context
def cli(ctx: click.Context, config: str) -> None:
    """Obsidian CLI tool"""
    ctx.obj = ObsidianContext(config)


def create_cli() -> click.Group:
    """Create the CLI application."""
    cli = click.Group()
    empty_notes_command.register_command(cli)
    small_notes_command.register_command(cli)
    empty_folders_command.register_command(cli)
    daily_stats_command.register_command(cli)
    word_cloud_command.register_command(cli)
    find_similar_command.register_command(cli)
    return cli


def main() -> None:
    load_commands(cli)
    cli()


if __name__ == "__main__":
    main()
