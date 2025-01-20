"""Test fixtures for PyObsidian."""
from typing import Dict, List, Optional, Tuple
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil
import os
from click.testing import CliRunner

# Import mock_obsidian before importing core
import tests.mock_obsidian
from pyobsidian.core import Note, Config, Vault, ObsidianContext
from .mock_obsidian import MockContext, Link

@pytest.fixture(scope="session")
def test_vault_dir():
    """Create a temporary directory for the test vault."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture(autouse=True)
def mock_vault_operations(mocker, test_vault_dir):
    """Mock all file system operations."""
    # Mock Path operations
    mocker.patch('pathlib.Path.rglob', return_value=[])
    mocker.patch('pathlib.Path.exists', return_value=True)
    mocker.patch('pathlib.Path.is_file', return_value=True)
    mocker.patch('pathlib.Path.is_dir', return_value=True)
    mocker.patch('pathlib.Path.iterdir', return_value=[])
    mocker.patch('pathlib.Path.mkdir', return_value=None)
    mocker.patch('pathlib.Path.unlink', return_value=None)
    
    # Mock file operations
    mocker.patch('builtins.open', mocker.mock_open())
    mocker.patch('shutil.copytree', return_value=None)
    mocker.patch('shutil.rmtree', return_value=None)
    mocker.patch('os.makedirs', return_value=None)
    mocker.patch('os.path.exists', return_value=True)
    
    # Set up test environment
    os.environ['OBSIDIAN_VAULT_PATH'] = test_vault_dir

@pytest.fixture
def mock_vault(mocker):
    """Create a mock vault with fully mocked file operations."""
    # Create a class with all the methods we want to mock
    class MockVault:
        def __init__(self):
            self._notes = {}
            self._setup_test_notes()

        def _setup_test_notes(self):
            """Set up test notes with known word counts."""
            # note1.md: A test note with many words
            self._notes["note1.md"] = Note("note1.md", """# Test Note
This is a test note with many words. It has links to [[note2]] and [[note3]].
It also has some tags like #test and #python.
This note should have more than 5 words to test the small notes feature.""")

            # note2.md: An empty note
            self._notes["note2.md"] = Note("note2.md", "")

            # note3.md: A note about Python development
            self._notes["note3.md"] = Note("note3.md", """# Python Development
This note discusses Python development and testing.
It has a link back to [[note1]] and includes examples of code:
```python
def test():
    pass
```
This note also has more than 5 words.""")

            # note4.md: A short note
            self._notes["note4.md"] = Note("note4.md", "Just four words here. #short")

            # note5.md: A brief text
            self._notes["note5.md"] = Note("note5.md", "Just three words.")

            # note6.md: A note about programming
            self._notes["note6.md"] = Note("note6.md", "Two words.")

            # folder1/nested_note.md: A note about Python projects
            self._notes["folder1/nested_note.md"] = Note("folder1/nested_note.md", "Five words in this note.")

            # folder2/another_note.md: Another note
            self._notes["folder2/another_note.md"] = Note("folder2/another_note.md", "This note has more than five words.")

            # complex_note.md: A note with formatted links
            self._notes["complex_note.md"] = Note("complex_note.md", """# Complex Note
This note has various types of links:
- [[*italic link*]]
- [[**bold link**]]
- [[`code link`]]
- [["quoted link"]]
- [[spaced link name]]
- [[complex/path/to/note]]""")

            # python_note.md: A note about Python programming
            self._notes["python_note.md"] = Note("python_note.md", """# Python Programming
This note covers Python programming concepts.
It includes examples and best practices.""")

            # programming_note.md: A note about programming
            self._notes["programming_note.md"] = Note("programming_note.md", """# Programming
This note covers general programming concepts.
It includes examples and best practices.""")

            # unrelated_note.md: A note about cooking
            self._notes["unrelated_note.md"] = Note("unrelated_note.md", """# Cooking
This note is about cooking and recipes.
It has nothing to do with programming.""")

            # source.md: A source note for similarity testing
            self._notes["source.md"] = Note("source.md", """# Source Note
This is a source note for testing similarity.
It contains specific content for comparison.""")

            # empty.md: An empty note for similarity testing
            self._notes["empty.md"] = Note("empty.md", "")

        def exists(self, path: str) -> bool:
            return path in self._notes

        def is_file(self, path: str) -> bool:
            return path in self._notes

        def is_dir(self, path: str) -> bool:
            return path == "/mock/vault/empty_folder"

        def get_all_files(self) -> List[str]:
            return list(self._notes.keys())

        def get_folders(self) -> List[str]:
            return ["/mock/vault/empty_folder"]

        def read_file(self, path: str) -> str:
            return self._notes[path].content if path in self._notes else ""

        def write_file(self, path: str, content: str) -> None:
            self._notes[path] = Note(path, content)

        def get_note(self, path: str) -> Note:
            if path not in self._notes:
                raise ValueError(f"Note {path} not found")
            return self._notes[path]

        def get_all_notes(self) -> List[Note]:
            return list(self._notes.values())

        def get_all_tags(self) -> Dict[str, int]:
            tag_counts = {}
            for note in self._notes.values():
                for tag in note.tags:
                    tag = tag.lstrip('#')
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
            return tag_counts

        def get_notes_by_tag(self, tag: str) -> List[Note]:
            tag = f"#{tag.lstrip('#')}"
            return [note for note in self._notes.values() if tag in note.tags]

        def update_note(self, path: str, content: str) -> None:
            if path not in self._notes:
                raise ValueError(f"Note {path} not found")
            self._notes[path].update_content(content)

        def get_empty_notes(self) -> List[Note]:
            return [note for note in self._notes.values() if not note.content.strip()]

        def get_small_notes(self, max_words: int) -> List[Note]:
            return [note for note in self._notes.values() if note.word_count <= max_words]

        def get_broken_links(self) -> List[Tuple[str, str]]:
            broken_links = []
            for note in self._notes.values():
                for link in note.links:
                    if not self.exists(link.target):
                        broken_links.append((note.path, link.target))
            return broken_links

        def get_orphan_notes(self) -> List[Note]:
            linked_notes = set()
            for note in self._notes.values():
                for link in note.links:
                    linked_notes.add(link.target)
            return [note for note in self._notes.values() if note.path not in linked_notes]

        def get_statistics(self) -> Dict[str, int]:
            return {
                "total_notes": len(self._notes),
                "total_tags": len(self.get_all_tags()),
                "empty_notes": len(self.get_empty_notes()),
                "broken_links": len(self.get_broken_links()),
                "orphan_notes": len(self.get_orphan_notes())
            }

    # Create the mock with our custom class as spec
    vault = mocker.Mock(spec=MockVault())
    vault.vault_path = Path("/mock/vault")
    vault.folders = {
        "/mock/vault": [],
        "/mock/vault/folder1": [],
        "/mock/vault/folder2": []
    }
    
    # Set up all the mock methods
    vault.exists.side_effect = lambda path: path in vault._notes
    vault.is_file.side_effect = lambda path: path in vault._notes
    vault.is_dir.side_effect = lambda path: str(path) in vault.folders
    vault.get_note.side_effect = lambda path: vault._notes.get(path)
    vault.get_all_notes.side_effect = lambda: list(vault._notes.values())
    vault.get_all_files.side_effect = lambda: list(vault._notes.keys())
    vault.get_folders.side_effect = lambda: list(vault.folders.keys())
    vault.read_file.side_effect = lambda path: vault._notes[path].content if path in vault._notes else ""
    vault.write_file.side_effect = lambda path, content: vault._notes.update({path: Note(path, content)})
    vault.get_empty_notes.side_effect = lambda: [note for note in vault._notes.values() if not note.content.strip()]
    vault.get_small_notes.side_effect = lambda max_words: [note for note in vault._notes.values() if note.word_count <= max_words]
    vault.get_broken_links.side_effect = lambda: [note for note in vault._notes.values() if any(not vault.exists(link.target) for link in note.links)]
    vault.get_orphan_notes.side_effect = lambda: [note for note in vault._notes.values() if note.path not in {link.target for note in vault._notes.values() for link in note.links}]
    vault.get_all_tags.side_effect = lambda: {tag: sum(1 for note in vault._notes.values() if tag in note.tags) for tag in {tag for note in vault._notes.values() for tag in note.tags}}
    vault.get_notes_by_tag.side_effect = lambda tag: [note for note in vault._notes.values() if tag in note.tags]
    vault.search_notes.side_effect = lambda query, case_sensitive=False: [note for note in vault._notes.values() if (query.lower() in note.content.lower() if not case_sensitive else query in note.content)]
    
    # Mock visualization operations
    vault.create_graph_visualization = mocker.Mock(return_value=None)
    vault.create_tag_cloud = mocker.Mock(return_value=None)
    
    # Mock export operations
    vault.export_to_markdown = mocker.Mock(return_value=None)
    vault.export_to_html = mocker.Mock(return_value=None)
    
    # Mock backup operations
    vault.create_backup = mocker.Mock(return_value="/mock/backup/path")
    
    # Mock statistics operations
    vault.get_statistics = mocker.Mock(return_value={
        "total_notes": len(vault._notes),
        "total_tags": sum(len(note.tags) for note in vault._notes.values()),
        "total_links": sum(len(note.links) for note in vault._notes.values()),
        "total_folders": len(vault.folders)
    })
    
    return vault

@pytest.fixture
def mock_config(mocker):
    """Create a mock configuration."""
    # Create a class with all the methods we want to mock
    class MockConfig:
        def __init__(self):
            self.vault_path = "/mock/vault"
            self.excluded_patterns = []
            self.config_data = {"obsidian": {"vault_path": self.vault_path}}
        
        def get(self, key, default=None):
            return self.config_data.get("obsidian", {}).get(key, default)
    
    # Create the mock with our custom class as spec
    config = mocker.Mock(spec=MockConfig())
    config.vault_path = "/mock/vault"
    config.excluded_patterns = []
    config.config_data = {"obsidian": {"vault_path": config.vault_path}}
    config.get.side_effect = lambda key, default=None: config.config_data.get("obsidian", {}).get(key, default)
    
    return config

@pytest.fixture
def mock_context() -> MockContext:
    """Create a mock context for testing."""
    context = MockContext()
    
    # Mock visualization methods
    context.vault.create_graph_visualization = MagicMock(return_value=None)
    context.vault.create_tag_visualization = MagicMock(return_value=None)
    
    # Mock backup and export methods
    context.vault.create_backup = MagicMock(return_value="/mock/backup/path")
    context.vault.export_to_markdown = MagicMock(return_value=None)
    context.vault.export_to_html = MagicMock(return_value=None)
    
    # Mock update_note method
    def update_note(path: str, content: str) -> None:
        if path not in context.vault.notes:
            context.vault.notes[path] = Note(path, content)
        note = context.vault.notes[path]
        note._content = content
        # Update tags based on content
        note._tags = []
        for line in content.splitlines():
            if "#" in line:
                tags = [word.strip("#") for word in line.split() if word.startswith("#")]
                note._tags.extend(tags)
    context.vault.update_note = update_note
    
    return context

@pytest.fixture(autouse=True)
def mock_core():
    """Mock the core module."""
    with patch('pyobsidian.core.ObsidianContext') as mock_context:
        mock_context.return_value = MockContext()
        yield mock_context

@pytest.fixture(autouse=True)
def mock_click_locale():
    """Mock Click's locale handling."""
    with patch('click._compat.get_best_encoding', return_value='utf-8'):
        yield

@pytest.fixture(autouse=True)
def mock_gettext():
    """Mock gettext to avoid locale issues."""
    with patch('gettext.translation') as mock_translation:
        mock_translation.return_value.gettext = lambda x: x
        mock_translation.return_value.ngettext = lambda s, p, n: s if n == 1 else p
        yield

@pytest.fixture(autouse=True)
def set_test_env():
    """Set environment variables for testing."""
    os.environ['LANG'] = 'C.UTF-8'
    os.environ['LC_ALL'] = 'C.UTF-8'
    yield
    # Clean up is handled automatically by pytest 

@pytest.fixture
def mock_context():
    """Create a mock context for testing."""
    return MockContext()

def pytest_collection_modifyitems(items):
    """Modify test items in place to ensure test classes are run in order."""
    items.sort(key=lambda x: x.get_closest_marker('order').args[0] if x.get_closest_marker('order') else 0) 