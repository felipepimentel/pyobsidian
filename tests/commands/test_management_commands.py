"""Test management commands."""
import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch, MagicMock
from pyobsidian.commands import (
    tag_management_command,
    visualization_command,
    data_management_command,
    export_command,
)
from tests.mock_obsidian import MockContext, Note
import os

# Mock the global context at the module level
import pyobsidian.core
pyobsidian.core.obsidian_context = None

@pytest.fixture(autouse=True)
def setup_mock_context(mock_context: "MockContext", mocker) -> None:
    """Set up the mock context for each test."""
    # Mock gettext functionality
    mocker.patch('gettext.translation', return_value=Mock(gettext=lambda x: x))
    
    # Mock all output functions
    mocker.patch('click.echo', return_value=None)
    mocker.patch('rich.console.Console.print', return_value=None)
    mocker.patch('builtins.print', return_value=None)
    mocker.patch('sys.stdout.write', return_value=None)
    mocker.patch('sys.stderr.write', return_value=None)
    
    # Mock file operations
    mocker.patch('pathlib.Path.mkdir', return_value=None)
    mocker.patch('pathlib.Path.exists', return_value=False)
    mocker.patch('pathlib.Path.is_file', return_value=False)
    mocker.patch('pathlib.Path.is_dir', return_value=False)
    mocker.patch('shutil.copytree', return_value=None)
    mocker.patch('shutil.rmtree', return_value=None)
    
    # Mock the global context
    mocker.patch('pyobsidian.commands.tag_management_command.obsidian_context', mock_context)
    mocker.patch('pyobsidian.commands.visualization_command.obsidian_context', mock_context)
    mocker.patch('pyobsidian.commands.data_management_command.obsidian_context', mock_context)
    mocker.patch('pyobsidian.commands.export_command.obsidian_context', mock_context)

def test_tag_management(mock_context: MockContext) -> None:
    """Test tag management operations."""
    runner = CliRunner()
    
    # Test adding a tag
    result = runner.invoke(tag_management_command.add_tag, ["note1.md", "newtag"])
    assert result.exit_code == 0
    assert "#newtag" in mock_context.vault.get_note("note1.md").content
    
    # Test removing a tag
    result = runner.invoke(tag_management_command.remove_tag, ["note1.md", "newtag"])
    assert result.exit_code == 0
    assert "#newtag" not in mock_context.vault.get_note("note1.md").content
    
    # Test replacing a tag
    note = mock_context.vault.get_note("note1.md")
    note.add_tag("oldtag")
    mock_context.vault.update_note(note.path, note.content)
    result = runner.invoke(tag_management_command.replace_tag, ["oldtag", "newtag"])
    assert result.exit_code == 0
    assert "#oldtag" not in mock_context.vault.get_note("note1.md").content
    assert "#newtag" in mock_context.vault.get_note("note1.md").content
    assert "oldtag" not in mock_context.vault.get_note("note1.md").tags
    assert "newtag" in mock_context.vault.get_note("note1.md").tags

def test_visualization(mock_context: MockContext) -> None:
    """Test visualization commands."""
    runner = CliRunner()
    result = runner.invoke(visualization_command.visualize_graph)
    assert result.exit_code == 0
    assert mock_context.vault.create_graph_visualization.called

    result = runner.invoke(visualization_command.visualize_tags)
    assert result.exit_code == 0
    assert mock_context.vault.create_tag_cloud.called

def test_data_management(mock_context: MockContext) -> None:
    """Test data management commands."""
    # Mock os.path.exists and os.makedirs
    with patch("os.path.exists", return_value=False), patch("os.makedirs", return_value=None):
        runner = CliRunner()
        
        # Test backup creation
        result = runner.invoke(data_management_command.create_backup)
        assert result.exit_code == 0
        assert mock_context.vault.create_backup.call_count > 0
        
        # Test export to markdown
        result = runner.invoke(data_management_command.export_notes, ["--format", "markdown"])
        assert result.exit_code == 0
        assert mock_context.vault.export_to_markdown.call_count > 0
        
        # Test export to HTML
        result = runner.invoke(data_management_command.export_notes, ["--format", "html"])
        assert result.exit_code == 0
        assert mock_context.vault.export_to_html.call_count > 0

def test_export(mock_context: "MockContext") -> None:
    """Test export commands."""
    runner = CliRunner()
    result = runner.invoke(export_command.export_notes, ["--format", "markdown"])
    assert result.exit_code == 0
    assert mock_context.vault.export_to_markdown.called

    result = runner.invoke(export_command.export_notes, ["--format", "html"])
    assert result.exit_code == 0
    assert mock_context.vault.export_to_html.called 