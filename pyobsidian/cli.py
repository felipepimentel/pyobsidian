import importlib
import os

import click


@click.group()
def cli():
    pass


def register_commands(cli):
    scripts_dir = os.path.join(os.path.dirname(__file__), "scripts")
    for filename in os.listdir(scripts_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f".scripts.{filename[:-3]}"
            module = importlib.import_module(module_name, package="pyobsidian")
            if hasattr(module, "register_command"):
                module.register_command(cli)


def start_cli():
    cli()
    register_commands(cli)


if __name__ == "__main__":
    start_cli()
