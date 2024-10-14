import importlib
import os

import click

from .obsidian import load_config
from .notify import notify



def command_wrapper(func):
    def wrapper(*args, **kwargs):
        config = load_config()
        try:
            result = func(config, *args, **kwargs)
            if isinstance(result, tuple):
                message, notification = result
            else:
                message, notification = result, result
            click.echo(message)
            notify(*notification)
        except Exception as e:
            click.echo(f"Error: {str(e)}")

    return wrapper
