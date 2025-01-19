"""Tests for link commands."""
from typing import TYPE_CHECKING
from click.testing import CliRunner
from pyobsidian.commands import (
    orphan_links_command,
    broken_links_command
)

if TYPE_CHECKING:
    from ..conftest import MockContext


def test_orphan_notes(mock_context: "MockContext") -> None:
    """Test finding orphan notes."""
    runner = CliRunner()
    result = runner.invoke(orphan_links_command.orphan_notes)
    
    assert result.exit_code == 0
    assert "note6.md" in result.output  # No links to this note
    assert "note1.md" not in result.output  # Has incoming link


def test_orphan_notes_with_empty(mock_context: "MockContext") -> None:
    """Test finding orphan notes including empty ones."""
    runner = CliRunner()
    result = runner.invoke(orphan_links_command.orphan_notes, ["--include-empty"])
    
    assert result.exit_code == 0
    assert "note2.md" in result.output  # Empty note
    assert "note6.md" in result.output  # No links to this note
    assert "note1.md" not in result.output  # Has incoming link


def test_broken_links(mock_context: "MockContext") -> None:
    """Test finding broken links."""
    runner = CliRunner()
    result = runner.invoke(broken_links_command.broken_links)
    
    assert result.exit_code == 0
    assert "non-existent-note" in result.output  # Broken link target 