"""Command for analyzing daily writing statistics."""
from typing import Dict, List
from datetime import datetime, timedelta
import click

from ..core import obsidian_context
from ..ui_handler import display_table

@click.command()
@click.option('--days', default=7, help='Number of days to analyze')
def daily_stats(days: int) -> None:
    """Show writing statistics for recent days."""
    stats = _collect_daily_stats(days)
    _display_stats(stats)

def _collect_daily_stats(days: int) -> Dict[str, Dict[str, int]]:
    """Collect writing statistics for the specified number of days."""
    stats = {}
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Initialize stats for each day in the range
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        stats[date_str] = {
            "words": 0,
            "notes": 0,
            "links": 0
        }
        current_date += timedelta(days=1)

    # Collect stats for each note
    for note in obsidian_context.vault.get_all_notes():
        # Get note's modification date from metadata
        try:
            mod_date = datetime.fromtimestamp(note.path.stat().st_mtime)
            date_str = mod_date.strftime("%Y-%m-%d")
            if date_str in stats:  # Only count if within our date range
                stats[date_str]["words"] += note.word_count
                stats[date_str]["notes"] += 1
                stats[date_str]["links"] += len(note.links)
        except (OSError, AttributeError):
            # Skip if we can't get modification date
            continue

    return stats

def _display_stats(stats: Dict[str, Dict[str, int]]) -> None:
    """Display the collected statistics."""
    headers = ["Date", "Words Written", "Notes Modified", "Links Created"]
    rows = []
    for date, day_stats in sorted(stats.items(), reverse=True):
        rows.append([
            date,
            str(day_stats["words"]),
            str(day_stats["notes"]),
            str(day_stats["links"])
        ])
    display_table(rows, headers, "Daily Writing Statistics")

def register_command(cli: click.Group) -> None:
    """Register the daily-stats command."""
    cli.add_command(daily_stats, name="daily-stats") 