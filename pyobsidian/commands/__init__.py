from .broken_links_command import register_command as register_broken_links
from .small_notes_command import register_command as register_small_notes


def register_all_commands(cli):
    register_broken_links(cli)
    register_small_notes(cli)
