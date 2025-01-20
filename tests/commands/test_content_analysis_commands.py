"""Tests for content analysis commands."""
from typing import TYPE_CHECKING
import pytest
from click.testing import CliRunner
from pyobsidian.commands.small_notes_command import small_notes
from pyobsidian.commands.empty_notes_command import empty_notes
from pyobsidian.commands.empty_folders_command import empty_folders
from pyobsidian.note import Note

if TYPE_CHECKING:
    from ..conftest import MockContext

def test_empty_notes(mock_context: "MockContext") -> None:
    """Test finding empty notes."""
    runner = CliRunner()
    result = runner.invoke(empty_notes)
    
    assert result.exit_code == 0
    # note2.md is empty
    assert "note2.md" in result.output
    # note1.md has content
    assert "note1.md" not in result.output

def test_small_notes(mock_context):
    """Test finding notes with few words."""
    # Set up test notes with known word counts
    mock_context.vault.update_note("note1.md", "# Test Note\nThis is a test note. #python #testing #compound-tag #123numeric")
    mock_context.vault.update_note("note2.md", "")  # Empty note
    mock_context.vault.update_note("note3.md", "# Python Development\nThis is a longer note about Python development and testing.")
    mock_context.vault.update_note("note4.md", "A short note #programming")
    mock_context.vault.update_note("note5.md", "Brief text only")
    mock_context.vault.update_note("note6.md", "One #programming")
    mock_context.vault.update_note("table_note.md", "# Table Note\n| Header | Value |")
    
    runner = CliRunner()
    
    # Test with default threshold (5 words)
    result = runner.invoke(small_notes)
    assert result.exit_code == 0
    assert "note2.md" in result.output  # Empty note
    assert "note4.md" in result.output  # Short note
    assert "note5.md" in result.output  # Brief text
    assert "note6.md" in result.output  # One word note
    assert "note1.md" not in result.output  # Longer note
    assert "note3.md" not in result.output  # Longer note

def test_empty_folders(mock_context: "MockContext") -> None:
    """Test listing empty folders."""
    runner = CliRunner()
    result = runner.invoke(empty_folders)
    
    assert result.exit_code == 0
    assert "empty_folder" in result.output 

class MockVault:
    def __init__(self):
        self.notes = []
        self.empty_notes = []
        self.empty_folders = []

    def get_all_notes(self):
        return self.notes

    def get_empty_notes(self):
        return self.empty_notes

    def get_empty_folders(self):
        return self.empty_folders

    def get_small_notes(self, max_words=50):
        return [note for note in self.notes if note.word_count <= max_words]

    def get_note(self, path):
        for note in self.notes:
            if note.path == path:
                return note
        return None 