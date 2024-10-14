# pyobsidian/cli.py

import click

from .commands import register_all_commands
from .core import ObsidianContext
from .ui_handler import (
    confirm_action,
    display,
    display_error,
    display_success,
    prompt_input,
)


@click.group()
@click.option("--config", default="config.yaml", help="Path to config file")
@click.pass_context
def cli(ctx: click.Context, config: str) -> None:
    """Obsidian CLI tool"""
    ctx.obj = ObsidianContext(config)


# Register all commands
register_all_commands(cli)


def command_handler(command: str, ctx: ObsidianContext) -> None:
    if command == "list":
        display(ctx.vault.get_all_notes(), format="table", title="All Notes")
    elif command == "view":
        path = prompt_input("Enter note path")
        note = ctx.vault.get_note(path)
        if note:
            display(note.content, format="panel", title=note.title)
        else:
            display_error(f"Note not found: {path}")
    elif command == "create":
        title = prompt_input("Enter note title")
        content = prompt_input("Enter note content")
        try:
            note = ctx.vault.create_note(title, content)
            display_success(f"Note created: {note.path}")
        except Exception as e:
            display_error(str(e))
    elif command == "update":
        path = prompt_input("Enter note path")
        note = ctx.vault.get_note(path)
        if note:
            display(note.content, format="panel", title=note.title)
            if confirm_action("Do you want to update this note?"):
                new_content = prompt_input("Enter new content")
                try:
                    updated_note = ctx.vault.update_note(path, new_content)
                    display_success(f"Note updated: {updated_note.path}")
                except Exception as e:
                    display_error(str(e))
        else:
            display_error(f"Note not found: {path}")
    elif command == "delete":
        path = prompt_input("Enter note path")
        note = ctx.vault.get_note(path)
        if note:
            display(note.content, format="panel", title=note.title)
            if confirm_action("Are you sure you want to delete this note?"):
                try:
                    ctx.vault.delete_note(path)
                    display_success(f"Note deleted: {path}")
                except Exception as e:
                    display_error(str(e))
        else:
            display_error(f"Note not found: {path}")
    else:
        display_error("Invalid command")


def main() -> None:
    ctx = ObsidianContext()
    ctx.run(command_handler)


if __name__ == "__main__":
    cli()
