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
        self.source = source
        self.target = target
        self.alias = alias

    def __eq__(self, other: object) -> bool:
        """Compare two Link objects for equality.

        Args:
            other: The other Link object to compare with.

        Returns:
            bool: True if the links are equal, False otherwise.
        """
        if not isinstance(other, Link):
            return NotImplemented
        return (self.source == other.source and 
                self.target == other.target and 
                self.alias == other.alias)

    def __hash__(self) -> int:
        """Get the hash value of the Link object.

        Returns:
            int: The hash value.
        """
        return hash((self.source, self.target, self.alias))

    def __repr__(self) -> str:
        """Get a string representation of the Link object.

        Returns:
            str: The string representation.
        """
        if self.alias:
            return f"Link(source='{self.source}', target='{self.target}', alias='{self.alias}')"
        return f"Link(source='{self.source}', target='{self.target}')"

class Note:
    """Mock note for testing."""

    def __init__(self, path: str, content: str) -> None:
        """Initialize a note."""
        self._path = path
        self._content = content
        self._title = self._extract_title()
        self._links = self._extract_links()
        self._tags = self._extract_tags()
        self._word_count = self._calculate_word_count()

    @property
    def content(self) -> str:
        """Get the note's content."""
        return self._content

    def update_content(self, new_content: str) -> None:
        """Update the note's content and recalculate all properties."""
        self._content = new_content
        self._title = self._extract_title()
        self._links = self._extract_links()
        self._tags = self._extract_tags()
        self._word_count = self._calculate_word_count()

    def add_tag(self, tag: str) -> None:
        """Add a tag to the note."""
        tag = tag.strip('#')  # Remove # if present
        if tag not in self._tags:
            # Add the tag at the end of the content, before any trailing newlines
            content_lines = self._content.rstrip().split('\n')
            content_lines.append(f"#{tag}")
            new_content = '\n'.join(content_lines) + '\n'
            self.update_content(new_content)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the note."""
        tag = tag.strip('#')  # Remove # if present
        if tag in self._tags:
            # Remove the tag, preserving whitespace
            new_content = re.sub(f'\\s*#({tag})(?=\\s|$)', '', self._content)
            self.update_content(new_content)

    def _extract_title(self) -> str:
        """Extract the title from the note's content."""
        lines = self._content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return ""

    def _extract_links(self) -> List[Link]:
        """Extract all links from the note's content."""
        links = []
        # Split content into lines
        lines = self._content.split('\n')
        in_code_block = False
        
        # Process each line
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if not in_code_block:
                # Remove inline code before extracting links
                line = re.sub(r'`[^`]+`', '', line)
                # Match [[target]] or [[target|alias]]
                pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
                matches = re.finditer(pattern, line)
                for match in matches:
                    target = match.group(1).strip()
                    alias = match.group(2).strip() if match.group(2) else None
                    # Handle links with special characters
                    target = re.sub(r'[\[\]]', '', target)  # Remove any remaining brackets
                    if target:
                        links.append(Link(source=self._path, target=target, alias=alias))
        
        return links

    def _extract_tags(self) -> Set[str]:
        """Extract all tags from the note's content."""
        # Split content into lines
        lines = self._content.split('\n')
        in_code_block = False
        content_without_code = []
        
        # Remove code blocks
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith('```'):
                in_code_block = not in_code_block
                continue
            if not in_code_block:
                content_without_code.append(line)
        
        content = '\n'.join(content_without_code)
        # Remove inline code
        content = re.sub(r'`[^`]+`', '', content)
        # Match #tag, excluding tags in code blocks
        pattern = r'#([\w-]+)'
        return set(re.findall(pattern, content))

    @property
    def path(self) -> str:
        """Get the note's path."""
        return self._path

    @property
    def title(self) -> str:
        """Get the note's title."""
        return self._title

    @property
    def links(self) -> List[Link]:
        """Get the note's links."""
        return self._links

    @property
    def tags(self) -> Set[str]:
        """Get the note's tags."""
        return self._tags

    @property
    def word_count(self) -> int:
        """Get the note's word count."""
        return self._word_count

    def _calculate_word_count(self) -> int:
        """Calculate the word count of the note's content."""
        # Remove code blocks
        content = self._content
        cleaned_lines = []
        in_code_block = False
        for line in content.split('\n'):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if not in_code_block:
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Remove inline code
        content = re.sub(r'`[^`]+`', '', content)
        
        # Remove tags
        content = re.sub(r'#[\w-]+', '', content)
        
        # Remove links
        content = re.sub(r'\[\[.*?\]\]', '', content)
        
        # Remove headers
        content = re.sub(r'^#\s.*$', '', content, flags=re.MULTILINE)
        
        # Remove punctuation and normalize whitespace
        content = re.sub(r'[^\w\s]', ' ', content)
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Split into words and count only those with letters
        words = [word for word in content.split() if any(c.isalpha() for c in word)]
        
        # Count each word only once if it's not a common word
        common_words = {'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'and', 'or', 'but', 'is', 'are', 'was', 'were'}
        unique_words = []
        for word in words:
            word = word.lower()
            if word not in common_words and word not in unique_words:
                unique_words.append(word)
        
        return len(unique_words)

    def __repr__(self) -> str:
        """Get a string representation of the note."""
        return f"Note(path='{self._path}', title='{self._title}')"

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

    def __init__(self, path: Path) -> None:
        """Initialize a mock vault."""
        self.path = path
        self._vault_path = path
        self._notes = {}  # Dictionary to store notes
        self._tags = {}   # Dictionary to store tags
        self._folders = {
            str(path): [],  # Root folder
            str(path / "folder1"): [],  # Test folder 1
            str(path / "folder2"): [],  # Test folder 2
            str(path / "empty_folder"): []  # Empty folder for testing
        }

        # Initialize test notes
        test_notes = {
            "note1.md": """# Python Testing
This is a note about #python and #testing and more words to make it longer than the minimum word count.
It links to [[note3]].""",
            
            "note2.md": "",  # Empty note
            
            "note3.md": """# Broken Link Note
This note has a [[non-existent-note]] link.
It also links to [[note1]].""",
            
            "note4.md": """# Small Note
Just a few words.""",
            
            "note5.md": """# Documentation Note
A note about #documentation.""",
            
            "note6.md": """# Python Programming
A note about #programming.""",
            
            "folder1/nested_note.md": """# Nested Note
This note is in a folder.""",
            
            "folder2/another_note.md": """# Another Note
This is another nested note."""
        }

        # Create notes in memory and update folders
        for path, content in test_notes.items():
            note = Note(path, content)
            self._notes[path] = note
            folder = str(Path(path).parent)
            if folder != ".":
                full_folder_path = str(self.path / folder)
                if full_folder_path not in self._folders:
                    self._folders[full_folder_path] = []
                self._folders[full_folder_path].append(path)
            else:
                self._folders[str(self.path)].append(path)

    @property
    def notes(self) -> Dict[str, Note]:
        """Get all notes in the vault."""
        return self._notes

    @property
    def folders(self) -> Dict[str, List[str]]:
        """Get all folders in the vault."""
        return self._folders

    def get_empty_folders(self) -> List[str]:
        """Get a list of empty folders in the vault."""
        empty_folders = []
        for folder_path, notes in self._folders.items():
            if not notes and folder_path != str(self.path):  # If the folder has no notes and is not the root folder
                empty_folders.append(os.path.basename(folder_path))
        return sorted(empty_folders)

    def get_all_tags(self) -> Dict[str, int]:
        """Get all tags and their counts."""
        tag_counts = {}
        for note in self._notes.values():
            for tag in note.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return dict(sorted(tag_counts.items()))  # Sort for consistent output

    def get_notes_by_tag(self, tag: str) -> List[Note]:
        """Get all notes with a specific tag."""
        notes_with_tag = []
        for note in self._notes.values():
            if tag in note.tags:
                notes_with_tag.append(note)
        return sorted(notes_with_tag, key=lambda x: x.path)  # Sort for consistent output

    def note_exists(self, path: str) -> bool:
        """Check if a note exists."""
        return path in self._notes

    def get_orphan_notes(self, include_empty: bool = False) -> List[Note]:
        """Get a list of orphaned notes (notes with no incoming links)."""
        all_links = set()
        for note in self._notes.values():
            for link in note.links:
                all_links.add(link.target + '.md')  # Add .md extension to match note paths

        orphan_notes = []
        for path, note in self._notes.items():
            if path not in all_links:
                if include_empty:  # Always include if include_empty is True
                    orphan_notes.append(note)
                elif note.content.strip():  # Only include non-empty notes if include_empty is False
                    orphan_notes.append(note)
        return sorted(orphan_notes, key=lambda x: x.path)  # Sort for consistent output

    def get_broken_links(self) -> List[Link]:
        """Get all broken links in the vault."""
        broken_links = []
        for note in self._notes.values():
            for link in note.links:
                target_path = link.target + '.md'
                if not self.note_exists(target_path):
                    broken_links.append(link)
        return sorted(broken_links, key=lambda x: (x.source, x.target))

    def update_note(self, path: str, content: str) -> None:
        """Update a note's content."""
        old_note = self._notes.get(path)
        if old_note:
            # Remove old tags
            for tag in old_note.tags:
                if tag in self._tags:
                    self._tags[tag].discard(path)
                    if not self._tags[tag]:
                        del self._tags[tag]
        
        # Create or update note
        note = Note(path, content)
        self._notes[path] = note
        
        # Add new tags
        for tag in note.tags:
            if tag not in self._tags:
                self._tags[tag] = set()
            self._tags[tag].add(path)

    def get_note(self, path: str) -> Optional[Note]:
        """Get a note by its path."""
        return self._notes.get(path)

    def get_all_notes(self) -> List[Note]:
        """Get all notes in the vault."""
        return list(self._notes.values())

    def get_empty_notes(self) -> List[Note]:
        """Get empty notes."""
        return [note for note in self._notes.values() if not note.content.strip()]

    def get_small_notes(self, min_words: int = 5) -> List[Note]:
        """Get notes with fewer than min_words words."""
        small_notes = []
        for note in self._notes.values():
            # Skip empty notes
            if not note.content.strip():
                continue
            # Count words in note content
            if 0 < note.word_count < min_words:
                small_notes.append(note)
        return sorted(small_notes, key=lambda x: x.path)  # Sort for consistent output

    def read_file(self, path: str) -> str:
        """Read a file's content."""
        if path in self._notes:
            return self._notes[path].content
        return ""

    def write_file(self, path: str, content: str) -> None:
        """Write content to a file."""
        self.update_note(path, content)

    def exists(self, path: str) -> bool:
        """Check if a path exists."""
        return path in self._notes

    def is_file(self, path: str) -> bool:
        """Check if a path is a file."""
        return path in self._notes

    def is_dir(self, path: str) -> bool:
        """Check if a path is a directory."""
        return str(path) in self._folders

    def create_graph_visualization(self, output: Optional[str] = None) -> None:
        """Create a graph visualization."""
        pass

    def create_tag_cloud(self, output: Optional[str] = None) -> None:
        """Create a tag cloud visualization."""
        pass

    def create_backup(self) -> str:
        """Create a backup of the vault."""
        # Mock implementation - just record that the method was called
        return "/mock/backup/path"

    def export_to_markdown(self, output_dir: str) -> None:
        """Export vault to markdown files."""
        # Mock implementation - just record that the method was called
        pass

    def export_to_html(self, output_dir: str) -> None:
        """Export vault to HTML files."""
        # Mock implementation - just record that the method was called
        pass

    def __getattr__(self, name: str) -> Any:
        """Handle attribute access."""
        if name == 'notes':
            return self._notes
        return super().__getattr__(name)

class MockContext:
    """Mock context for testing."""

    def __init__(self) -> None:
        """Initialize a mock context."""
        self._vault = MockVault(Path("/mock/vault"))
        
        # Initialize mock methods with proper return values
        self._vault.read_file = MagicMock(side_effect=self._vault.read_file)
        self._vault.write_file = MagicMock(side_effect=self._vault.write_file)
        self._vault.exists = MagicMock(side_effect=self._vault.exists)
        self._vault.is_file = MagicMock(side_effect=self._vault.is_file)
        self._vault.is_dir = MagicMock(side_effect=self._vault.is_dir)
        self._vault.create_graph_visualization = MagicMock()
        self._vault.create_tag_cloud = MagicMock()
        self._vault.create_backup = MagicMock(return_value="/mock/backup/path")
        self._vault.export_to_markdown = MagicMock()
        self._vault.export_to_html = MagicMock()
        self._vault.update_note = MagicMock(side_effect=self._vault.update_note)

    @property
    def vault(self) -> MockVault:
        """Get the mock vault."""
        return self._vault

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