"""Command to find similar notes based on content similarity."""
from typing import Dict, List, Set, Tuple
from collections import Counter, defaultdict
import math
import click
from ..core import obsidian_context
from ..ui_handler import display_table, display_success
import re
from ..note import Note
from rich.table import Table
from rich.console import Console

def _get_note_words(content: str) -> Set[str]:
    """Get a set of words from note content."""
    # Convert to lowercase and split into words
    words = content.lower().split()
    
    # Filter words
    filtered = set()
    for word in words:
        # Skip tags and links
        if word.startswith('#') or word.startswith('[['):
            continue
            
        # Remove punctuation and normalize
        word = ''.join(c for c in word if c.isalnum())
        
        # Skip if too short or no letters
        if len(word) <= 2 or not any(c.isalpha() for c in word):
            continue
            
        filtered.add(word)
    
    return filtered

def _calculate_tf_idf_similarity(source_words: Set[str], target_words: Set[str], 
                               idf_scores: Dict[str, float]) -> Tuple[float, List[str]]:
    """Calculate TF-IDF weighted similarity between two sets of words."""
    if not source_words or not target_words:
        return 0.0, []
    
    # Create TF-IDF vectors
    source_vector = defaultdict(float)
    target_vector = defaultdict(float)
    
    # Calculate TF-IDF for source
    for word in source_words:
        if word in idf_scores:
            source_vector[word] = idf_scores[word]
            
    # Calculate TF-IDF for target
    for word in target_words:
        if word in idf_scores:
            target_vector[word] = idf_scores[word]
    
    # Calculate cosine similarity
    dot_product = sum(source_vector[word] * target_vector[word] 
                     for word in set(source_vector) & set(target_vector))
    
    source_norm = math.sqrt(sum(score * score for score in source_vector.values()))
    target_norm = math.sqrt(sum(score * score for score in target_vector.values()))
    
    if source_norm == 0 or target_norm == 0:
        return 0.0, []
        
    similarity = dot_product / (source_norm * target_norm)
    
    # Get common significant terms
    common_terms = sorted(
        set(source_vector) & set(target_vector),
        key=lambda w: source_vector[w] * target_vector[w],
        reverse=True
    )[:3]
    
    return similarity, common_terms

def _clean_text(content: str) -> str:
    """Clean text by removing YAML frontmatter, code blocks, headers, links, and tags."""
    # Remove YAML frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`[^`]+`', '', content)
    
    # Remove headers
    content = re.sub(r'^#+\s.*$', '', content, flags=re.MULTILINE)
    
    # Remove links and tags
    content = re.sub(r'\[\[.*?\]\]', '', content)
    content = re.sub(r'#\w+', '', content)
    
    # Convert to lowercase and remove punctuation
    content = re.sub(r'[^\w\s]', ' ', content.lower())
    
    return content

def _calculate_similarity(source_note: Note, note: Note) -> float:
    """Calculate similarity between two notes."""
    # Skip empty notes
    if not source_note.content.strip() or not note.content.strip():
        return 0.0

    # Check for identical content after stripping whitespace
    if source_note.content.strip() == note.content.strip():
        return 1.0

    # Get words from both notes
    words1 = set(_get_words(source_note.content))
    words2 = set(_get_words(note.content))

    # Calculate base similarity using Jaccard similarity
    common_words = words1 & words2
    all_words = words1 | words2
    if not all_words:
        return 0.0
    base_similarity = len(common_words) / len(all_words)

    # Calculate programming topic similarity
    programming_words = {'python', 'code', 'development', 'testing', 'programming'}
    words1_prog = words1 & programming_words
    words2_prog = words2 & programming_words
    prog_similarity = len(words1_prog & words2_prog) / max(1, len(words1_prog | words2_prog)) if words1_prog or words2_prog else 0.0

    # Calculate bidirectional link similarity
    has_bidirectional_links = (
        any(link.target == note.path.removesuffix('.md') for link in source_note.links) and
        any(link.target == source_note.path.removesuffix('.md') for link in note.links)
    )

    # Calculate code block similarity
    has_code_blocks = bool(re.search(r'```.*?```', source_note.content, re.DOTALL)) and bool(re.search(r'```.*?```', note.content, re.DOTALL))

    # Base similarity score
    similarity = base_similarity

    # Apply boosts
    if has_code_blocks:
        similarity *= 3.0
    if has_bidirectional_links:
        similarity *= 3.0
    if prog_similarity > 0:
        similarity *= 3.0

    return min(1.0, similarity)

def _get_words(content: str) -> List[str]:
    """Extract words from note content."""
    # Remove code blocks and inline code
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`.*?`', '', content)
    # Remove headers
    content = re.sub(r'^#+ .*$', '', content, flags=re.MULTILINE)
    # Remove links and tags
    content = re.sub(r'\[\[([^\]]+)\]\]', '', content)
    content = re.sub(r'#\w+', '', content)
    # Remove emphasis markers
    content = re.sub(r'(\*\*|\*|__|_)', '', content)
    # Convert to lowercase and split into words
    words = content.lower().split()
    # Filter words
    return [word for word in words if len(word) >= 2 and any(c.isalpha() for c in word)]

@click.command()
@click.argument('note_path', type=str)
@click.option('--min-similarity', default=0.1, help='Minimum similarity threshold.')
@click.option('--limit', default=10, help='Maximum number of similar notes to display.')
def find_similar(note_path: str, min_similarity: float, limit: int) -> None:
    """Find notes similar to the given note."""
    try:
        source_note = obsidian_context.vault.get_note(note_path)
    except ValueError:
        display_table([], ["Path", "Title", "Similarity", "Tags"], title=f"Notes similar to {note_path}")
        return

    # Skip empty notes
    if not source_note.content.strip():
        display_table([], ["Path", "Title", "Similarity", "Tags"], title=f"Notes similar to {note_path}")
        return

    # Calculate similarities
    similarities = []
    for note in obsidian_context.vault.get_all_notes():
        if note.path == source_note.path:
            continue
        similarity = _calculate_similarity(source_note, note)
        if similarity >= min_similarity:
            similarities.append((note, similarity))

    # Sort by similarity and limit results
    similarities.sort(key=lambda x: (-x[1], x[0].path))
    similarities = similarities[:limit]

    # Prepare rows for display
    rows = []
    for note, similarity in similarities:
        rows.append([
            note.path,
            note.title,
            f"{similarity * 100:.1f}%",
            ' '.join(f'#{tag}' for tag in note.tags)
        ])

    display_table(rows, ["Path", "Title", "Similarity", "Tags"], title=f"Notes similar to {note_path}")

def register_command(cli: click.Group) -> None:
    """Register the find-similar command to the CLI group."""
    cli.add_command(find_similar, name="find-similar") 