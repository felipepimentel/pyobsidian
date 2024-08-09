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

@cli.command()
def generate_report():
    from .obsidian_helper import load_config
    from .scripts.generate_reports import generate_report
    from .scripts.notify import notify
    
    config = load_config()
    report_file = generate_report(config)
    
    click.echo(f"Report generated: {report_file}")
    notify("Report Generation", f"Report file created: {report_file}")

@cli.command()
def identify_broken_links():
    from .obsidian_helper import load_config
    from .scripts.identify_broken_links import identify_broken_links
    from .scripts.notify import notify
    
    config = load_config()
    broken_links = identify_broken_links(config)
    
    click.echo(f"Identified {len(broken_links)} broken links")
    notify("Broken Links", f"{len(broken_links)} broken links identified")

@cli.command()
def identify_duplicate_notes():
    from .obsidian_helper import load_config
    from .scripts.identify_duplicate_notes import identify_duplicate_notes
    from .scripts.notify import notify
    
    config = load_config()
    duplicates = identify_duplicate_notes(config)
    
    click.echo(f"Identified {len(duplicates)} duplicate notes")
    notify("Duplicate Notes", f"{len(duplicates)} duplicate notes identified")

@cli.command()
def identify_small_notes():
    from .obsidian_helper import load_config
    from .scripts.identify_empty_notes import identify_small_notes
    from .scripts.notify import notify
    
    config = load_config()
    small_notes = identify_small_notes(config)
    
    click.echo(f"Identified {len(small_notes)} small notes")
    notify("Small Notes", f"{len(small_notes)} small notes identified")

@cli.command()
def identify_unused_images():
    from .obsidian_helper import load_config
    from .scripts.identify_unused_images import identify_unused_images
    from .scripts.notify import notify
    
    config = load_config()
    unused_images = identify_unused_images(config)
    
    click.echo(f"Identified {len(unused_images)} unused images")
    notify("Unused Images", f"{len(unused_images)} unused images identified")

@cli.command()
def incremental_backup():
    from .obsidian_helper import load_config
    from .scripts.incremental_backup import incremental_backup
    from .scripts.notify import notify
    
    config = load_config()
    backup_file = incremental_backup(config)
    
    click.echo(f"Incremental backup created: {backup_file}")
    notify("Incremental Backup", f"Backup file created: {backup_file}")

@cli.command()
def manage_tasks():
    from .obsidian_helper import load_config
    from .scripts.manage_tasks import manage_tasks
    from .scripts.notify import notify
    
    config = load_config()
    task_summary = manage_tasks(config)
    
    click.echo(f"Task management completed: {task_summary}")
    notify("Task Management", f"Task summary: {task_summary}")

@cli.command()
def merge_agenda_notes():
    from .obsidian_helper import load_config
    from .scripts.merge_agenda_notes import merge_agenda_notes
    from .scripts.notify import notify
    
    config = load_config()
    merged_note = merge_agenda_notes(config)
    
    click.echo(f"Agenda notes merged: {merged_note}")
    notify("Agenda Merge", f"Merged agenda note created: {merged_note}")

@cli.command()
def sync_git():
    from .obsidian_helper import load_config
    from .scripts.sync_with_git import sync_with_git
    from .scripts.notify import notify
    
    config = load_config()
    sync_result = sync_with_git(config)
    
    click.echo(f"Git sync completed: {sync_result}")
    notify("Git Sync", f"Sync result: {sync_result}")

@cli.command()
def visualize_data():
    from .obsidian_helper import load_config
    from .scripts.visualize_data import visualize_data
    from .scripts.notify import notify
    
    config = load_config()
    visualization_file = visualize_data(config)
    
    click.echo(f"Data visualization created: {visualization_file}")
    notify("Data Visualization", f"Visualization file created: {visualization_file}")

@cli.command()
def process_voice_notes():
    from .obsidian_helper import load_config
    from .scripts.voice_notes import process_voice_notes
    from .scripts.notify import notify
    
    config = load_config()
    processed_notes = process_voice_notes(config)
    
    click.echo(f"Processed {len(processed_notes)} voice notes")
    notify("Voice Notes", f"{len(processed_notes)} voice notes processed")

if __name__ == "__main__":
    cli()
