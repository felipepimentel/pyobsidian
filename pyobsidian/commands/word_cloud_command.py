"""Command to generate a word cloud from notes."""
from typing import Dict, List
import click
import re
from collections import Counter

from ..core import obsidian_context
from ..ui_handler import display_table, display_error

# Common English stop words to filter out
STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
    'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were',
    'will', 'with', 'this', 'but', 'they', 'have', 'had', 'what', 'when',
    'where', 'who', 'which', 'why', 'how'
}

@click.command()
@click.option('--min-length', default=3, help='Minimum word length')
@click.option('--min-count', default=2, help='Minimum word count')
@click.option('--max-words', default=5, help='Maximum number of words to display')
def word_cloud(min_length: int, min_count: int, max_words: int) -> None:
    """Generate a word cloud from notes."""
    notes = obsidian_context.vault.get_all_notes()
    word_counts = Counter()
    
    for note in notes:
        # Get content and remove code blocks
        content = note._remove_code_blocks(note._content)
        
        # Remove links and tags
        content = re.sub(r'\[\[.*?\]\]', '', content)
        content = re.sub(r'#\w+', '', content)
        
        # Remove headers
        content = re.sub(r'^#+\s.*$', '', content, flags=re.MULTILINE)
        
        # Remove formatting and punctuation
        content = re.sub(r'[*_`]', '', content)
        content = re.sub(r'[^\w\s]', ' ', content)
        
        # Normalize whitespace
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        # Count words
        words = content.lower().split()
        word_counts.update(w for w in words if len(w) >= min_length and w not in STOP_WORDS)
        
        # Include words from tags (without the #)
        for tag in note.tags:
            tag = tag.lower()
            if len(tag) >= min_length and tag not in STOP_WORDS:
                word_counts[tag] += 1
    
    # Filter and sort words
    filtered_words = {word: count for word, count in word_counts.items() if count >= min_count}
    sorted_words = sorted(filtered_words.items(), key=lambda x: (-x[1], x[0]))[:max_words]
    
    # If no words found, display message
    if not sorted_words:
        display_table([], ["Word", "Count", "Percentage"], title="No words found meeting the criteria")
        return
    
    # Calculate total for percentages
    total_count = sum(count for _, count in sorted_words)
    
    # Prepare rows for display
    rows = []
    for word, count in sorted_words:
        percentage = (count / total_count) * 100
        rows.append([word, str(count), f"{percentage:.1f}%"])
    
    display_table(rows, ["Word", "Count", "Percentage"], 
                 title=f"Word Cloud (min length: {min_length}, min count: {min_count})")

def register_command(cli: click.Group) -> None:
    """Register the word-cloud command to the CLI group."""
    cli.add_command(word_cloud, name="word-cloud") 