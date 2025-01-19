@click.command(cls=BaseCommand, name="empty-folders")
def empty_folders() -> None:
    """List empty folders in the vault."""
    empty_folders = obsidian_context.vault.get_empty_folders()
    display_folders(empty_folders, title="Empty Folders") 