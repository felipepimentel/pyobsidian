import click
from .scripts import ai_assistant
from .scripts import advanced_visualizations
from .scripts import cloud_sync
from .scripts import smart_tags
from .scripts import note_recommender
from .scripts import spaced_repetition
from .scripts import quote_extractor
from .scripts import productivity_analysis
from .scripts import knowledge_graph
from .scripts import realtime_collaboration
from .scripts import ai_insights
from .plugin_system import PluginSystem
from .web_interface import run_web_interface

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

@cli.command()
@click.argument('note_path')
def enhance_note(note_path):
    """Enhance a note using AI."""
    enhanced_note = ai_assistant.enhance_note(note_path)
    click.echo(f"Note enhanced: {enhanced_note}")

@cli.command()
@click.argument('topic')
def generate_ideas(topic):
    """Generate note ideas on a topic using AI."""
    ideas = ai_assistant.generate_note_ideas(topic)
    click.echo(f"Ideas for {topic}:\n{ideas}")

@cli.command()
def visualize_tags():
    """Visualize tag evolution over time."""
    config = load_config()
    output_path = advanced_visualizations.visualize_tag_evolution(config)
    click.echo(f"Tag evolution visualization saved to: {output_path}")

@cli.command()
def sync_dropbox():
    """Sync vault to Dropbox."""
    config = load_config()
    result = cloud_sync.sync_to_dropbox(config)
    click.echo(result)

@cli.command()
def apply_smart_tags():
    """Apply smart tags to all notes based on content."""
    config = load_config()
    result = smart_tags.apply_smart_tags(config)
    click.echo(result)

@cli.command()
@click.argument('note_path')
@click.option('--num', default=5, help='Number of recommendations')
def recommend_related(note_path, num):
    """Recommend related notes based on content similarity."""
    config = load_config()
    related_notes = note_recommender.get_related_notes(config, note_path, num)
    click.echo(f"Notes related to {note_path}:")
    for note in related_notes:
        click.echo(note)

@cli.command()
def visualize_note_length():
    """Visualize note length distribution over time."""
    config = load_config()
    output_path = advanced_visualizations.visualize_note_length_distribution(config)
    click.echo(f"Note length distribution visualization saved to: {output_path}")

@cli.command()
def review_notes():
    """Get notes for review based on spaced repetition."""
    config = load_config()
    notes_to_review = spaced_repetition.update_review_dates(config)
    click.echo(f"Notes to review today: {len(notes_to_review)}")
    for note in notes_to_review:
        click.echo(note)

@cli.command()
def extract_quotes():
    """Extract and summarize quotes from all notes."""
    config = load_config()
    summary_path = quote_extractor.generate_quote_summary(config)
    click.echo(f"Quote summary generated: {summary_path}")

@cli.command()
@click.option('--days', default=30, help='Number of days to analyze')
def analyze_productivity(days):
    """Analyze productivity based on note modifications."""
    config = load_config()
    output_path = productivity_analysis.analyze_productivity(config, days)
    click.echo(f"Productivity analysis generated: {output_path}")

@cli.command()
def generate_knowledge_graph():
    """Generate a knowledge graph based on note connections."""
    config = load_config()
    graph_path = knowledge_graph.generate_knowledge_graph(config)
    click.echo(f"Knowledge graph generated: {graph_path}")

@cli.command()
def analyze_vault():
    """Analyze the entire vault using AI."""
    config = load_config()
    analysis_path = ai_assistant.analyze_vault(config)
    click.echo(f"Vault analysis generated: {analysis_path}")

@cli.command()
def list_plugins():
    """List all available plugins."""
    config = load_config()
    plugin_system = PluginSystem(config['plugin_dir'])
    plugin_system.load_plugins()
    plugins = plugin_system.list_plugins()
    click.echo("Available plugins:")
    for plugin in plugins:
        click.echo(f"- {plugin}")

@cli.command()
@click.argument('plugin_name')
@click.argument('args', nargs=-1)
def run_plugin(plugin_name, args):
    """Run a specific plugin."""
    config = load_config()
    plugin_system = PluginSystem(config['plugin_dir'])
    plugin_system.load_plugins()
    result = plugin_system.execute_plugin(plugin_name, *args)
    click.echo(f"Plugin {plugin_name} executed. Result: {result}")

@cli.command()
def start_web_interface():
    """Start the web interface."""
    run_web_interface()

@cli.command()
def start_collaboration_server():
    """Start the real-time collaboration server."""
    config = load_config()
    collaboration = realtime_collaboration.RealtimeCollaboration(config)
    click.echo("Starting real-time collaboration server...")
    collaboration.start_server()

@cli.command()
def generate_ai_insights():
    """Generate AI insights based on the entire vault content."""
    config = load_config()
    insight_path = ai_insights.generate_ai_insights(config)
    click.echo(f"AI insights generated: {insight_path}")

if __name__ == "__main__":
    cli()
