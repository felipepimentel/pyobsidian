"""Tests for word cloud command."""
import pytest
from click.testing import CliRunner
from pyobsidian.commands import word_cloud_command
from ..mock_obsidian import MockContext

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