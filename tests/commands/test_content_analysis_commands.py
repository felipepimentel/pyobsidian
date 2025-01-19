"""Tests for content analysis commands."""
from typing import TYPE_CHECKING
import pytest
from click.testing import CliRunner
from pyobsidian.commands import (
    empty_notes_command,
    small_notes_command,
    empty_folders_command
)

if TYPE_CHECKING:
    from ..conftest import MockContext

def test_empty_notes(mock_context: "MockContext") -> None:
    """Test finding empty notes."""
    runner = CliRunner()
    result = runner.invoke(empty_notes_command.empty_notes, catch_exceptions=False)
    
    assert result.exit_code == 0
    # note2.md is empty
    assert "note2.md" in result.output
    # note1.md has content
    assert "note1.md" not in result.output
    # Verify no physical files were accessed
    assert not mock_context.vault.read_file.called

def test_small_notes(mock_context: "MockContext") -> None:
    """Test finding small notes."""
    runner = CliRunner()
    
    # Test with default threshold (5 words)
    result = runner.invoke(small_notes_command.small_notes)
    assert result.exit_code == 0
    # "Just a few words" is 4 words
    assert "note4.md" in result.output
    # Empty notes should not be included
    assert "note2.md" not in result.output
    # Notes with more than 5 words should not be included
    assert "note1.md" not in result.output
    # Verify no physical files were accessed
    assert not mock_context.vault.read_file.called
    
    # Test with custom threshold (10 words)
    result = runner.invoke(small_notes_command.small_notes, ["--min-words", "10"])
    assert result.exit_code == 0
    # Should include notes with less than 10 words
    assert "note4.md" in result.output  # 4 words
    assert "note5.md" in result.output  # "A note about #documentation" is 4 words
    assert "note6.md" in result.output  # "A note about #programming" is 4 words
    # Should not include empty notes
    assert "note2.md" not in result.output
    # Should not include notes with more than 10 words
    assert "note1.md" not in result.output
    # Verify no physical files were accessed
    assert not mock_context.vault.read_file.called

def test_empty_folders(mock_context: "MockContext") -> None:
    """Test listing empty folders."""
    # The mock vault already has an empty folder configured in its initialization
    runner = CliRunner()
    result = runner.invoke(empty_folders_command.empty_folders)
    
    assert result.exit_code == 0
    assert "empty_folder" in result.output
    # Verify no physical files were accessed
    assert not mock_context.vault.read_file.called 