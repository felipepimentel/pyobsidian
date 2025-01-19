"""Tests for search commands."""
from typing import TYPE_CHECKING
from click.testing import CliRunner
from pyobsidian.commands import list_tags_command, notes_by_tag_command

if TYPE_CHECKING:
    from ..conftest import MockContext


def test_list_tags(mock_context: "MockContext") -> None:
    """Test listing all tags."""
    runner = CliRunner()
    result = runner.invoke(list_tags_command.list_tags)
    
    assert result.exit_code == 0
    assert "python" in result.output
    assert "testing" in result.output
    assert "programming" in result.output
    assert "documentation" in result.output


def test_notes_by_tag(mock_context: "MockContext") -> None:
    """Test finding notes by tag."""
    runner = CliRunner()
    
    # Test with existing tag
    result = runner.invoke(notes_by_tag_command.notes_by_tag, ["python"])
    assert result.exit_code == 0
    assert "note1.md" in result.output
    
    # Test with non-existent tag
    result = runner.invoke(notes_by_tag_command.notes_by_tag, ["nonexistent"])
    assert result.exit_code == 0
    assert "No notes found" in result.output 