"""Mock ObsidianContext for testing."""
from unittest.mock import Mock, MagicMock
from pathlib import Path
import types
from typing import Optional, Union, List, Any, Set, Dict, Tuple
import re
import os

from pyobsidian.core import Config, Note, Vault

# Create mock classes
class Link:
    """A class representing a link between notes."""

    def __init__(self, source: str, target: str, alias: Optional[str] = None) -> None:
        """Initialize a link."""
        self._source = source
        self._target = target.strip()
        self._alias = alias.strip() if alias else None

    @property
    def source(self) -> str:
        """Get the source note or path."""
        return self._source

    @property
    def target(self) -> str:
        """Get the target path."""
        return self._target.removesuffix('.md')  # Remove .md suffix if present

    @property
    def alias(self) -> Optional[str]:
        """Get the link alias."""
        return self._alias

    def __eq__(self, other: object) -> bool:
        """Compare links for equality."""
        if not isinstance(other, Link):
            return NotImplemented
        return (self.source == other.source and 
                self.target == other.target and 
                self.alias == other.alias)

    def __lt__(self, other: "Link") -> bool:
        """Compare links for sorting."""
        return (self.source, self.target) < (other.source, other.target)

    def __repr__(self) -> str:
        """Get a string representation of the link."""
        return f"Link(source='{self.source}', target='{self.target}', alias={self.alias})"

class Note:
    """Mock note for testing."""

    def __init__(self, path: str, content: str = "") -> None:
        """Initialize a mock note."""
        self._path = path
        self._content = content
        self._title = self._extract_title()
        self._tags = self._extract_tags()
        self._links = self._extract_links()

    @property
    def path(self) -> str:
        """Get the note's path."""
        return self._path

    @property
    def content(self) -> str:
        """Get the note's content."""
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        """Set the note's content."""
        self.update_content(value)

    def update_content(self, content: str) -> None:
        """Update the note's content."""
        self._content = content
        self._title = self._extract_title()
        self._tags = self._extract_tags()
        self._links = self._extract_links()

    def _extract_title(self) -> str:
        """Extract the title from the note's content."""
        lines = self._content.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("# "):
                title = line[2:].strip()
                title = re.sub(r'(\*\*|\*|__|_)', '', title)
                return title
        return ""

    def _extract_tags(self) -> List[str]:
        """Extract tags from the note's content."""
        # First remove code blocks
        content = self._remove_code_blocks(self._content)
        # Find all tags
        pattern = r'#([a-zA-Z0-9][\w-]*(?:-[\w-]+)*)'
        matches = re.finditer(pattern, content)
        
        # Keep track of seen tags to avoid duplicates
        seen = set()
        tags = []
        
        for match in matches:
            tag = match.group(1)
            # Skip invalid tags
            if tag.startswith('!') or tag.startswith('-') or tag.endswith('-'):
                continue
            # Skip tags with emphasis markers
            if any(marker in tag for marker in ['*', '_', '`']):
                continue
            if tag not in seen:
                seen.add(tag)
                tags.append(tag)
        
        return sorted(tags)

    def _extract_links(self) -> List[Link]:
        """Extract links from the note's content."""
        links = []
        seen = set()
        # First remove code blocks
        content = self._remove_code_blocks(self._content)
        # Find all links in the remaining content
        for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
            target = match.group(1)
            if '|' in target:
                target, alias = target.split('|', 1)
            else:
                alias = target
            # Handle markdown links inside wikilinks
            if target.startswith('[') and '](' in target:
                target = target[1:].split('](')[0]
            # Clean up target and alias
            target = target.strip()
            alias = alias.strip()
            # Handle complex paths
            if '/' in target:
                target = target.split('/')[-1]
            # Handle quoted links
            if target.startswith('"') and target.endswith('"'):
                target = target[1:-1]
            # Handle emphasis markers
            target = re.sub(r'(\*\*|\*|__|_|`|```)', '', target)
            # Handle markdown links
            if target.startswith('[') and target.endswith(']'):
                target = target[1:-1]
            if target not in seen:
                seen.add(target)
                links.append(Link(target, alias))
        return sorted(links)

    def _remove_code_blocks(self, content: str) -> str:
        """Remove code blocks from content."""
        return re.sub(r'```[^`]*```', '', content)

    def _remove_inline_code(self, content: str) -> str:
        """Remove inline code from content."""
        return re.sub(r'`[^`]+`', '', content)

    def _remove_tags(self, content: str) -> str:
        """Remove tags from content."""
        return re.sub(r'#[^\s#]+', '', content)

    def _remove_links(self, content: str) -> str:
        """Remove links from content."""
        return re.sub(r'\[\[([^\]]+)\]\]', '', content)

    def _remove_headers(self, content: str) -> str:
        """Remove headers from content."""
        return re.sub(r'^#+ .*$', '', content, flags=re.MULTILINE)

    def _normalize_whitespace(self, content: str) -> str:
        """Normalize whitespace in content."""
        return ' '.join(content.split())

    def _calculate_word_count(self) -> int:
        """Calculate the number of words in the note's content."""
        content = self._content
        # Remove code blocks and inline code
        content = self._remove_code_blocks(content)
        content = self._remove_inline_code(content)
        # Remove tags and links
        content = self._remove_tags(content)
        content = self._remove_links(content)
        # Remove headers
        content = self._remove_headers(content)
        # Remove emphasis markers
        content = re.sub(r'(\*\*|\*|__|_)', '', content)
        # Remove punctuation and numbers
        content = re.sub(r'[^\w\s]|[\d]', ' ', content)
        # Normalize whitespace
        content = self._normalize_whitespace(content)
        # Split into words and filter
        words = [w for w in content.split() if len(w) > 1 and any(c.isalpha() for c in w)]
        # Remove duplicates
        words = list(dict.fromkeys(words))
        return len(words)

    def add_tag(self, tag: str) -> None:
        """Add a tag to the note."""
        if not tag.startswith('#'):
            tag = f'#{tag}'
        if tag not in self._content:
            if self._content.strip():
                self._content = self._content.rstrip() + f' {tag}\n'
            else:
                self._content = f'{tag}\n'

    @property
    def title(self) -> str:
        """Get the note's title."""
        return self._extract_title()

    @property
    def tags(self) -> List[str]:
        """Get the note's tags."""
        return self._extract_tags()

    @property
    def links(self) -> List[Link]:
        """Get the note's links."""
        return self._extract_links()

    @property
    def word_count(self) -> int:
        """Get the note's word count."""
        return self._calculate_word_count()

    def __lt__(self, other: 'Note') -> bool:
        """Compare notes by path."""
        return self.path < other.path

    def __repr__(self) -> str:
        """Get a string representation of the note."""
        return f"Note(path='{self.path}', title='{self.title}')"

class Config:
    """Mock configuration."""
    def __init__(self):
        self.vault_path = "/mock/vault"
        self.excluded_patterns = []
        self.config_data = {"obsidian": {"vault_path": self.vault_path}}

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config_data.get("obsidian", {}).get(key, default)

class MockVault:
    """Mock vault for testing."""

    def __init__(self) -> None:
        """Initialize the mock vault."""
        self._notes = {}
        self.folders = {"empty_folder"}  # Add empty folder for testing
        
        # Mock methods
        self._read_file = Mock()
        self._write_file = Mock()
        self._create_graph_visualization = Mock()
        self._create_tag_cloud = Mock()
        self._create_backup = Mock(return_value="/mock/backup/path")
        self._export_to_markdown = Mock()
        self._export_to_html = Mock()

        self._setup_test_notes()

    @property
    def read_file(self) -> Mock:
        """Get the mock read_file method."""
        return self._read_file

    @property
    def write_file(self) -> Mock:
        """Get the mock write_file method."""
        return self._write_file

    @property
    def create_graph_visualization(self) -> Mock:
        """Get the mock create_graph_visualization method."""
        return self._create_graph_visualization

    @property
    def create_tag_cloud(self) -> Mock:
        """Get the mock create_tag_cloud method."""
        return self._create_tag_cloud

    @property
    def create_backup(self) -> Mock:
        """Get the mock create_backup method."""
        return self._create_backup

    @property
    def export_to_markdown(self) -> Mock:
        """Get the mock export_to_markdown method."""
        return self._export_to_markdown

    @property
    def export_to_html(self) -> Mock:
        """Get the mock export_to_html method."""
        return self._export_to_html

    @property
    def notes(self) -> Dict[str, Note]:
        """Get all notes as a dictionary."""
        return self._notes

    def add_note(self, path: str, content: str = "") -> None:
        """Add a note to the vault."""
        self._notes[path] = Note(path, content)
        # Add parent folders
        parts = path.split('/')
        if len(parts) > 1:
            folder = '/'.join(parts[:-1])
            self.folders.add(folder)

    def update_note(self, path: str, content: str) -> None:
        """Update a note's content."""
        if path in self._notes:
            self._notes[path].update_content(content)

    def get_orphan_notes(self) -> List[Note]:
        """Get notes that no other notes link to."""
        linked_to = set()
        for note in self._notes.values():
            for link in note.links:
                linked_to.add(link.target)
        
        orphans = []
        for note in self._notes.values():
            if note.path.removesuffix('.md') not in linked_to:
                orphans.append(note)
        
        return sorted(orphans)

    def get_broken_links(self) -> List[Tuple[Note, List[Link]]]:
        """Get all broken links in the vault."""
        broken = []
        for note in self._notes.values():
            broken_links = []
            for link in note.links:
                target_path = link.target + '.md'
                if target_path not in self._notes:
                    broken_links.append(link)
            if broken_links:
                broken.append((note, broken_links))
        return sorted(broken, key=lambda x: x[0].path)

    def get_all_notes(self) -> List[Note]:
        """Get all notes in the vault."""
        return sorted(self._notes.values())

    def get_empty_notes(self) -> List[Note]:
        """Get notes with no content."""
        return sorted(note for note in self._notes.values() if not note.content.strip())

    def get_empty_folders(self) -> List[str]:
        """Get folders that contain no notes."""
        used_folders = set()
        for path in self._notes:
            parts = path.split('/')
            if len(parts) > 1:
                folder = '/'.join(parts[:-1])
                used_folders.add(folder)
        
        return sorted(folder for folder in self.folders if folder not in used_folders)

    def note_exists(self, path: str) -> bool:
        """Check if a note exists."""
        return path in self._notes or path + '.md' in self._notes

    def get_all_tags(self) -> Dict[str, int]:
        """Get all tags and their counts from notes."""
        tag_counts = {}
        for path, content in self._notes.items():
            note = Note(path, content)
            for tag in note.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return tag_counts

    def get_notes_by_tag(self, tag: str) -> List[Note]:
        """Get all notes that contain a specific tag."""
        matching_notes = []
        for path, content in self._notes.items():
            note = Note(path, content)
            if tag in note.tags:
                matching_notes.append(note)
        return sorted(matching_notes)

    def _get_note(self, note_path: str) -> Note:
        """Get a note by its path."""
        if note_path not in self._notes:
            raise ValueError(f"Note {note_path} not found")
        return self._notes[note_path]

    def get_note(self, note_path: str) -> Note:
        """Get a note by its path."""
        return self._get_note(note_path)

    def _setup_test_notes(self):
        """Set up test notes with specific content."""
        # Add test notes
        self.add_note("note1.md", """# Test Note
This is a test note. #python #testing #compound-tag #123numeric
It has some content about Python programming.
This note links to [[note2]] and [[note3]].""")
        
        self.add_note("note2.md", "")  # Empty note
        
        self.add_note("note3.md", """# Python Development
This note has Python examples and code.
It also links to [[note1]] and discusses programming.
Python is a great language for testing.""")
        
        self.add_note("note4.md", "A brief note about #programming.")
        
        self.add_note("note5.md", "Another brief note.")
        
        self.add_note("note6.md", "A note about #programming")  # 4 words
        
        self.add_note("folder1/nested_note.md", """# Python Projects
This note is about Python projects and development.
It covers various aspects of Python programming.""")
        
        # Add notes for find_similar tests
        self.add_note("python_note.md", """# Python
This is a note about Python programming concepts.
It covers basic Python syntax and features.""")
        
        self.add_note("programming_note.md", """# Programming
This note covers general programming concepts.
It discusses various programming paradigms.""")
        
        self.add_note("unrelated_note.md", """# Cooking
This is about cooking recipes.
It has nothing to do with programming.""")
        
        self.add_note("source.md", """# Source Note
This is the source note for testing similarity.
It contains various programming concepts.""")
        
        self.add_note("empty.md", "")  # Empty note for similarity test
        
        # Add notes for link tests
        self.add_note("complex_note.md", """# Complex Note
This note has various link types:
- [[bold link|**Bold Link**]]
- [[italic link|*Italic Link*]]
- [[code link|`Code Link`]]
- [[code block link|```Code Block Link```]]
- [[markdown link|[Markdown Link](http://example.com)]]
- [[quoted link|"Quoted Link"]]
- [[complex/path/to/note]]
""")
        
        # Add notes for table tests
        self.add_note("table_note.md", """# Table Note
| Column 1 | Column 2 |
|----------|----------|
| [[link1]] | [[link2]] |
| [[link3]] | [[link4]] |
""")

class MockContext:
    """Mock ObsidianContext for testing."""

    def __init__(self) -> None:
        """Initialize the mock context."""
        self._vault = MockVault()
        
        # Add test notes
        self._vault.add_note("note1.md", "# Test Note\nThis is a test note. #python #testing #compound-tag #123numeric")
        self._vault.add_note("note2.md", "")  # Empty note
        self._vault.add_note("note3.md", "This note links to [[note1]] and [[non-existent-note]].")
        self._vault.add_note("note4.md", "A brief note about #programming.")
        self._vault.add_note("note5.md", "Another brief note.")
        self._vault.add_note("note6.md", "A note about #programming")  # 4 words
        self._vault.add_note("folder1/nested_note.md", "This is a nested note.")
        
        # Add notes for find_similar tests
        self._vault.add_note("python_note.md", "# Python\nThis is a note about Python programming concepts.")
        self._vault.add_note("programming_note.md", "# Programming\nThis note covers general programming concepts.")
        self._vault.add_note("unrelated_note.md", "# Cooking\nThis is about cooking recipes.")
        self._vault.add_note("source.md", "# Source Note\nThis is the source note for testing similarity.")
        self._vault.add_note("empty.md", "")  # Empty note for similarity test
        
        # Add notes for link tests
        self._vault.add_note("complex_note.md", """# Complex Note
This note has various link types:
- [[bold link|**Bold Link**]]
- [[italic link|*Italic Link*]]
- [[code link|`Code Link`]]
- [[code block link|```Code Block Link```]]
- [[markdown link|[Markdown Link](http://example.com)]]
- [[quoted link|"Quoted Link"]]
- [[complex/path/to/note]]
""")

        # Add notes for table tests
        self._vault.add_note("table_note.md", """# Table Note
| Column 1 | Column 2 |
|----------|----------|
| [[link1]] | [[link2]] |
| [[link3|Alias]] | [[link4]] |
""")

    @property
    def vault(self) -> MockVault:
        """Get the mock vault."""
        return self._vault

    @property
    def config(self) -> Config:
        """Get the mock config."""
        return Config()

    @vault.setter
    def vault(self, value: MockVault) -> None:
        """Set the mock vault."""
        self._vault = value

    def __getattr__(self, name: str) -> Any:
        """Handle attribute access."""
        if name == 'notes':
            return self._vault._notes
        return super().__getattr__(name)

# Create a mock module
mock_core = types.ModuleType('pyobsidian.core')
mock_core.Note = Note
mock_core.Link = Link
mock_core.Config = Config
mock_core.Vault = MockVault
mock_core.ObsidianContext = Mock()
mock_core.ObsidianContext.return_value = MockContext()
mock_core.obsidian_context = MockContext()

# Add the mock module to sys.modules
import sys
sys.modules['pyobsidian.core'] = mock_core

# Ensure that the Note class is not mocked
def note_getattr(self, name):
    """Handle attribute access for Note objects."""
    if name.startswith('_'):
        return object.__getattribute__(self, name)
    if name == 'notes':
        return object.__getattribute__(self, '_notes')
    if name == 'folders':
        return object.__getattribute__(self, '_folders')
    return object.__getattribute__(self, f'_{name}')

def note_getitem(self, key):
    """Handle dictionary-like access for Note objects."""
    return getattr(self, f"_{key}")

def note_iter(self):
    """Handle iteration for Note objects."""
    return iter(self._content)

Note.__getattr__ = note_getattr
Note.__getitem__ = note_getitem
Note.__iter__ = note_iter

# Ensure that the mock vault's notes are not mocked
def vault_getattr(self, name):
    """Handle attribute access for Vault objects."""
    if name == 'notes':
        return object.__getattribute__(self, '_notes')
    if name == 'folders':
        return object.__getattribute__(self, '_folders')
    if name.startswith('_'):
        return object.__getattribute__(self, name)
    return object.__getattribute__(self, f'_{name}')

def vault_getitem(self, key):
    """Handle dictionary-like access for Vault objects."""
    return getattr(self, f"_{key}")

MockVault.__getattr__ = vault_getattr
MockVault.__getitem__ = vault_getitem

# Ensure that the mock vault's methods are properly called
def vault_call(self, *args, **kwargs):
    """Handle method calls for Vault objects."""
    return None

MockVault.__call__ = vault_call

__all__ = ['MockContext', 'Note', 'Link', 'Config', 'MockVault'] 