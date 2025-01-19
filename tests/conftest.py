"""Test fixtures for PyObsidian."""
from typing import Dict, List, Optional
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
            self.vault_path = Path("/mock/vault")
            self.notes = {}
            self.folders = {
                "/mock/vault": [],
                "/mock/vault/folder1": [],
                "/mock/vault/folder2": []
            }
            
            # Initialize with test notes
            test_notes = {
                "note1.md": """# Python Note
This is a note about #python and #testing.
It links to [[note2]] and [[note3]].""",
                
                "note2.md": """# Empty Note
""",
                
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
            
            # Create notes in memory
            for path, content in test_notes.items():
                note = Note(path, content)
                self.notes[path] = note
                
                # Update folder structure
                folder = str(Path(path).parent)
                if folder != ".":
                    full_folder_path = str(self.vault_path / folder)
                    if full_folder_path not in self.folders:
                        self.folders[full_folder_path] = []
                    self.folders[full_folder_path].append(path)
        
        def exists(self, path): return path in self.notes
        def is_file(self, path): return path in self.notes
        def is_dir(self, path): return str(path) in self.folders
        def get_note(self, path): return self.notes.get(path)
        def get_all_notes(self): return list(self.notes.values())
        def _get_all_files(self): return list(self.notes.keys())
        def get_folders(self): return list(self.folders.keys())
        def read_file(self, path): return self.notes[path].content if path in self.notes else ""
        def write_file(self, path, content): self.notes.update({path: Note(path, content)})
        def create_graph_visualization(self): return None
        def create_tag_cloud(self): return None
        def export_to_markdown(self, path): return None
        def export_to_html(self, path): return None
        def create_backup(self): return "/mock/backup/path"
        def get_statistics(self): return {
            "total_notes": len(self.notes),
            "total_tags": sum(len(note.tags) for note in self.notes.values()),
            "total_links": sum(len(note.links) for note in self.notes.values()),
            "total_folders": len(self.folders)
        }
        def note_exists(self, path): return path in self.notes
        def get_empty_notes(self): return [note for note in self.notes.values() if not note.content.strip()]
        def get_small_notes(self, min_words=50): return [note for note in self.notes.values() if note.word_count < min_words]
        def get_broken_links(self): return [note for note in self.notes.values() if any(not self.note_exists(link.target) for link in note.links)]
        def get_orphan_notes(self, include_empty=False): 
            all_links = {link.target for note in self.notes.values() for link in note.links}
            return [note for note in self.notes.values() if note.path not in all_links and (include_empty or note.content.strip())]
        def get_all_tags(self): return {tag: sum(1 for note in self.notes.values() if tag in note.tags) for tag in {tag for note in self.notes.values() for tag in note.tags}}
        def get_notes_by_tag(self, tag): return [note for note in self.notes.values() if tag in note.tags]
        def search_notes(self, query, case_sensitive=False): 
            if not case_sensitive:
                query = query.lower()
                return [note for note in self.notes.values() if query in note.content.lower()]
            return [note for note in self.notes.values() if query in note.content]
    
    # Create the mock with our custom class as spec
    vault = mocker.Mock(spec=MockVault())
    vault.vault_path = Path("/mock/vault")
    vault.notes = {}
    vault.folders = {
        "/mock/vault": [],
        "/mock/vault/folder1": [],
        "/mock/vault/folder2": []
    }
    
    # Set up all the mock methods
    vault.exists.side_effect = lambda path: path in vault.notes
    vault.is_file.side_effect = lambda path: path in vault.notes
    vault.is_dir.side_effect = lambda path: str(path) in vault.folders
    vault.get_note.side_effect = lambda path: vault.notes.get(path)
    vault.get_all_notes.side_effect = lambda: list(vault.notes.values())
    vault._get_all_files.side_effect = lambda: list(vault.notes.keys())
    vault.get_folders.side_effect = lambda: list(vault.folders.keys())
    vault.read_file.side_effect = lambda path: vault.notes[path].content if path in vault.notes else ""
    vault.write_file.side_effect = lambda path, content: vault.notes.update({path: Note(path, content)})
    vault.note_exists.side_effect = lambda path: path in vault.notes
    vault.get_empty_notes.side_effect = lambda: [note for note in vault.notes.values() if not note.content.strip()]
    vault.get_small_notes.side_effect = lambda min_words=50: [note for note in vault.notes.values() if note.word_count < min_words]
    vault.get_broken_links.side_effect = lambda: [note for note in vault.notes.values() if any(not vault.note_exists(link.target) for link in note.links)]
    vault.get_orphan_notes.side_effect = lambda include_empty=False: [note for note in vault.notes.values() if note.path not in {link.target for note in vault.notes.values() for link in note.links} and (include_empty or note.content.strip())]
    vault.get_all_tags.side_effect = lambda: {tag: sum(1 for note in vault.notes.values() if tag in note.tags) for tag in {tag for note in vault.notes.values() for tag in note.tags}}
    vault.get_notes_by_tag.side_effect = lambda tag: [note for note in vault.notes.values() if tag in note.tags]
    vault.search_notes.side_effect = lambda query, case_sensitive=False: [note for note in vault.notes.values() if (query.lower() in note.content.lower() if not case_sensitive else query in note.content)]
    
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
        "total_notes": len(vault.notes),
        "total_tags": sum(len(note.tags) for note in vault.notes.values()),
        "total_links": sum(len(note.links) for note in vault.notes.values()),
        "total_folders": len(vault.folders)
    })
    
    # Initialize test notes
    test_notes = {
        "note1.md": """# Python Note
This is a note about #python and #testing.
It links to [[note2]] and [[note3]].""",
        
        "note2.md": """# Empty Note
""",
        
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
    
    # Create notes in memory
    for path, content in test_notes.items():
        note = Note(path, content)
        vault.notes[path] = note
        
        # Update folder structure
        folder = str(Path(path).parent)
        if folder != ".":
            full_folder_path = str(vault.vault_path / folder)
            if full_folder_path not in vault.folders:
                vault.folders[full_folder_path] = []
            vault.folders[full_folder_path].append(path)
    
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