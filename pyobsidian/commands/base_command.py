"""Base command functionality for PyObsidian."""
import click

class BaseCommand(click.Command):
    """Base class for PyObsidian commands."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = kwargs.get('name', self.callback.__name__ if self.callback else None) 