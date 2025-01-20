"""Tests for daily stats command."""
from typing import TYPE_CHECKING
import pytest
from datetime import datetime, timedelta
from click.testing import CliRunner
from pyobsidian.commands import daily_stats_command
from unittest.mock import patch

if TYPE_CHECKING:
    from ..conftest import MockContext

def test_daily_stats(mock_context: "MockContext") -> None:
    """Test daily writing statistics command."""
    runner = CliRunner()
    
    # Mock file modification time
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    # Mock Path.stat() to return different modification times
    def mock_stat(path):
        if "note1.md" in str(path):
            return type('Stat', (), {'st_mtime': today.timestamp()})
        elif "note2.md" in str(path):
            return type('Stat', (), {'st_mtime': yesterday.timestamp()})
        return type('Stat', (), {'st_mtime': today.timestamp()})
    
    with patch('pathlib.Path.stat', side_effect=mock_stat):
        result = runner.invoke(daily_stats_command.daily_stats)
        
        assert result.exit_code == 0
        # Verify statistics are displayed
        assert "Daily Writing Statistics" in result.output
        assert "Words Written" in result.output
        assert "Notes Modified" in result.output
        assert "Links Created" in result.output
        # Verify dates are shown
        assert today.strftime("%Y-%m-%d") in result.output
        assert yesterday.strftime("%Y-%m-%d") in result.output
        # Verify no physical files were accessed
        assert not mock_context.vault.read_file.called

def test_daily_stats_with_days(mock_context: "MockContext") -> None:
    """Test daily stats with custom number of days."""
    runner = CliRunner()
    
    # Mock dates for the last 14 days
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(14)]
    
    # Mock Path.stat() to distribute notes across dates
    def mock_stat(path):
        # Distribute notes evenly across the date range
        index = hash(str(path)) % len(dates)
        return type('Stat', (), {'st_mtime': datetime.strptime(dates[index], "%Y-%m-%d").timestamp()})
    
    with patch('pathlib.Path.stat', side_effect=mock_stat):
        result = runner.invoke(daily_stats_command.daily_stats, ["--days", "14"])
        
        assert result.exit_code == 0
        assert "Daily Writing Statistics" in result.output
        # Verify multiple dates are shown
        for date in dates[:5]:  # Check at least some dates
            assert date in result.output

def test_daily_stats_handles_errors(mock_context: "MockContext") -> None:
    """Test daily stats handles file access errors gracefully."""
    runner = CliRunner()
    
    def mock_stat_error(path):
        raise OSError("Mock file access error")
    
    with patch('pathlib.Path.stat', side_effect=mock_stat_error):
        result = runner.invoke(daily_stats_command.daily_stats)
        
        assert result.exit_code == 0
        assert "Daily Writing Statistics" in result.output
        # Should show zeros for stats when files can't be accessed
        assert "0" in result.output 