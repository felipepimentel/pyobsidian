import click

@click.group()
def cli():
    pass

@cli.command()
def backup():
    from .obsidian_helper import load_config
    from .scripts.backup_and_export import backup_vault
    from .scripts.notify import notify
    
    config = load_config()
    backup_file = backup_vault(config)
    
    click.echo(f"Backup created: {backup_file}")
    notify("Backup", f"Backup file created: {backup_file}")

@cli.command()
def export_html():
    from .obsidian_helper import load_config
    from .scripts.backup_and_export import export_notes_to_html
    from .scripts.notify import notify
    
    config = load_config()
    export_dir = export_notes_to_html(config)
    
    click.echo(f"Notes exported to HTML: {export_dir}")
    notify("HTML Export", f"Notes exported to: {export_dir}")

@cli.command()
def analyze_content():
    from .obsidian_helper import load_config
    from .scripts.analyze_content import analyze_content
    from .scripts.notify import notify
    
    config = load_config()
    analysis_file = analyze_content(config)
    
    click.echo(f"Content analysis generated: {analysis_file}")
    notify("Content Analysis", f"Analysis file created: {analysis_file}")

@cli.command()
def archive_old():
    from .obsidian_helper import load_config
    from .scripts.archive_old_notes import archive_old_notes
    from .scripts.notify import notify
    
    config = load_config()
    archived_notes = archive_old_notes(config)
    
    click.echo(f"Archived {len(archived_notes)} old notes")
    notify("Note Archiving", f"{len(archived_notes)} notes archived")

@cli.command()
def manage_tags():
    from .obsidian_helper import load_config
    from .scripts.tag_management import manage_tags
    from .scripts.notify import notify
    
    config = load_config()
    tag_file = manage_tags(config)
    
    click.echo(f"Tag summary generated: {tag_file}")
    notify("Tag Management", f"Tag summary file created: {tag_file}")

@cli.command()
def daily_note():
    from .obsidian_helper import load_config
    from .scripts.daily_note_generator import generate_daily_note
    from .scripts.notify import notify
    
    config = load_config()
    daily_note_file = generate_daily_note(config)
    
    click.echo(f"Daily note generated: {daily_note_file}")
    notify("Daily Note", f"Daily note created: {daily_note_file}")

@cli.command()
def analyze_links():
    from .obsidian_helper import load_config
    from .scripts.link_analyzer import analyze_links
    from .scripts.notify import notify
    
    config = load_config()
    analysis_file = analyze_links(config)
    
    click.echo(f"Link analysis generated: {analysis_file}")
    notify("Link Analysis", f"Link analysis file created: {analysis_file}")

@cli.command()
@click.argument('template_name')
@click.argument('note_name')
def create_note(template_name, note_name):
    from .obsidian_helper import load_config
    from .scripts.note_templating import create_note_from_template
    from .scripts.notify import notify
    
    config = load_config()
    new_note_path = create_note_from_template(config, template_name, note_name)
    
    click.echo(f"New note created from template: {new_note_path}")
    notify("Note Creation", f"New note created: {new_note_path}")

@cli.command()
def list_templates():
    from .obsidian_helper import load_config
    from .scripts.note_templating import list_templates
    
    config = load_config()
    templates = list_templates(config)
    
    click.echo("Available templates:")
    for template in templates:
        click.echo(f"- {template}")

@cli.command()
def check_plugin_updates():
    from .obsidian_helper import load_config
    from .scripts.plugin_manager import check_for_updates
    from .scripts.notify import notify
    
    config = load_config()
    updates = check_for_updates(config)
    
    if updates:
        click.echo("Plugin updates available:")
        for plugin in updates:
            click.echo(f"- {plugin['name']}: {plugin['current_version']} -> {plugin['latest_version']}")
        notify("Plugin Updates", f"{len(updates)} plugin updates available")
    else:
        click.echo("All plugins are up to date.")
        notify("Plugin Updates", "All plugins are up to date")

if __name__ == "__main__":
    cli()
