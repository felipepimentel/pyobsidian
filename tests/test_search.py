import pytest
import os
import tempfile
from pyobsidian.search import Search
from pyobsidian.note_manager import NoteManager

@pytest.fixture
def temp_vault():
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.environ['OBSIDIAN_VAULT_PATH'] = tmpdirname
        yield tmpdirname

def test_search_notes(temp_vault):
    note_manager = NoteManager()
    note_manager.create_note("Note 1", "This is a test note with some content.")
    note_manager.create_note("Note 2", "Another note with different content.")

    search = Search()
    results = search.search_notes("test")

    assert "Note 1" in results
    assert "Note 2" not in results

def test_search_by_tag(temp_vault):
    note_manager = NoteManager()
    note_manager.create_note("Note 1", tags=["tag1", "tag2"])
    note_manager.create_note("Note 2", tags=["tag2", "tag3"])

    search = Search()
    results = search.search_by_tag("tag2")

    assert set(results) == {"Note 1", "Note 2"}

def test_search_by_date(temp_vault):
    note_manager = NoteManager()
    note_manager.create_note("Note 1")
    note_manager.create_note("Note 2")

    search = Search()
    note1 = note_manager.get_note("Note 1")
    note2 = note_manager.get_note("Note 2")

    start_date = min(note1['date'], note2['date'])
    end_date = max(note1['date'], note2['date'])

    results = search.search_by_date(start_date, end_date)

    assert set(results) == {"Note 1", "Note 2"}
