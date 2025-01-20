"""Tests for word cloud command."""
import pytest
from click.testing import CliRunner
from pyobsidian.commands import word_cloud_command
from ..mock_obsidian import MockContext

def test_word_cloud(mock_context: MockContext) -> None:
    """Test word cloud command."""
    runner = CliRunner()
    result = runner.invoke(word_cloud_command.word_cloud)
    
    assert result.exit_code == 0
    assert "Word Cloud" in result.output
    # Common words in test notes
    assert "python" in result.output.lower()
    assert "note" in result.output.lower()
    assert "test" in result.output.lower()
    # Verify percentages are shown
    assert "%" in result.output
    # Stop words should not appear
    for stop_word in ["the", "and", "is", "in", "to"]:
        assert stop_word not in result.output.lower()

def test_word_cloud_with_options(mock_context: MockContext) -> None:
    """Test word cloud command with custom options."""
    runner = CliRunner()
    result = runner.invoke(word_cloud_command.word_cloud, 
                         ["--min-count", "2", "--max-words", "5"])
    
    assert result.exit_code == 0
    assert "Word Cloud" in result.output
    # Should only show words that appear at least twice
    assert "note" in result.output.lower()  # Common word in test notes
    # Should show at most 5 words
    word_lines = [line for line in result.output.split('\n') if line.strip() and not line.startswith(('Word', '-'))]
    assert len(word_lines) <= 5

def test_word_cloud_filters(mock_context: MockContext) -> None:
    """Test word cloud filtering functionality."""
    # Add a note with various elements to filter
    mock_context.vault.update_note("test_filters.md", """
    # Test Filters
    This is a test with #tags and [[links]]
    Some `inline code` and short a an the words
    ```python
    code_block = "should be ignored"
    ```
    """)
    
    runner = CliRunner()
    result = runner.invoke(word_cloud_command.word_cloud)
    
    assert result.exit_code == 0
    # Tags and links should be filtered out
    assert "tags" not in result.output.lower()
    assert "links" not in result.output.lower()
    # Code should be filtered out
    assert "code_block" not in result.output.lower()
    assert "should" not in result.output.lower()
    assert "ignored" not in result.output.lower()
    # Short words should be filtered out
    assert " a " not in result.output.lower()
    assert " an " not in result.output.lower()
    assert " the " not in result.output.lower()

def test_word_cloud_empty_results(mock_context: MockContext) -> None:
    """Test word cloud handles empty results gracefully."""
    # Add a note with only stop words and filtered content
    mock_context.vault.update_note("empty_test.md", """
    # Empty Test
    a an the and or
    #tag [[link]]
    ```code```
    """)
    
    runner = CliRunner()
    result = runner.invoke(word_cloud_command.word_cloud, ["--min-count", "999"])
    
    assert result.exit_code == 0
    assert "No words found meeting the criteria" in result.output 