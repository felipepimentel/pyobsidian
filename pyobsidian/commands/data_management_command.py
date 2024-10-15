import re
from collections import defaultdict
from typing import Dict, List

import click

from ..core import obsidian_context
from ..ui_handler import display_sensitive_data


@click.group()
def data_management() -> None:
    """Commands for data management and security."""
    pass


@data_management.command()
@click.option("--verbose", is_flag=True, help="Show detailed pattern matches")
def detect_sensitive_data(verbose: bool) -> None:
    """Identify notes containing potentially sensitive information."""
    vault = obsidian_context.vault
    notes = vault.get_all_notes()
    sensitive_patterns = {
        "Credit Card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "Email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "SSN": r"\b(?:\d{3}-\d{2}-\d{4}|\d{9})\b",
    }
    sensitive_notes: Dict[str, Dict[str, List[str]]] = defaultdict(
        lambda: defaultdict(list)
    )

    for note in notes:
        for pattern_name, pattern in sensitive_patterns.items():
            matches = re.findall(pattern, note.content)
            if matches:
                sensitive_notes[note.title][pattern_name].extend(matches)

    display_sensitive_data(sensitive_notes, verbose)


def register_command(cli: click.Group) -> None:
    """Register the data management commands to the CLI group."""
    cli.add_command(data_management)
