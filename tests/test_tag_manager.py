import pytest
import os
import tempfile
from pyobsidian.tag_manager import TagManager
from pyobsidian.note_manager import NoteManager

@pytest.fixture
def temp_vault():
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.environ['OBSIDIAN_VAULT_PATH'] = tmpdirname
        yield tmpdirname

def test_list_tags(temp_vault):
    note_manager = NoteManager()
    note_manager.create_note("Note 1", tags=["tag1", "tag2"])
    note_manager.create_note("Note 2", tags=["tag2", "tag3"])

    tag_manager = TagManager()
    tags = tag_manager.list_tags()

    assert set(tags) == {"tag1", "tag2", "tag3"}

def test_get_notes_by_tag(temp_vault):
    note_manager = NoteManager()
    note_manager.create_note("Note 1", tags=["tag1", "tag2"])
    note_manager.create_note("Note 2", tags=["tag2", "tag3"])
    note_manager.create_note("Note 3", tags=["tag1", "tag3"])

    tag_manager = TagManager()
    notes_with_tag2 = tag_manager.get_notes_by_tag("tag2")

    assert set(notes_with_tag2) == {"Note 1", "Note 2"}

def test_add_tag_to_note(temp_vault):
    note_manager = NoteManager()
    note_manager.create_note("Test Note", tags=["initial"])

    tag_manager = TagManager()
    result = tag_manager.add_tag_to_note("Test Note", "new_tag")

    assert result is True
    updated_note = note_manager.get_note("Test Note")
    assert set(updated_note['tags']) == {"initial", "new_tag"}

def test_remove_tag_from_note(temp_vault):
    note_manager = NoteManager()
    note_manager.create_note("Test Note", tags=["tag1", "tag2"])

    tag_manager = TagManager()
    result = tag_manager.remove_tag_from_note("Test Note", "tag1")

    assert result is True
    updated_note = note_manager.get_note("Test Note")
    assert set(updated_note['tags']) == {"tag2"}
