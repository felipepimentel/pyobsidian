import pytest
import os
import tempfile
from pyobsidian.note_manager import NoteManager

@pytest.fixture
def temp_vault():
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.environ['OBSIDIAN_VAULT_PATH'] = tmpdirname
        yield tmpdirname

def test_create_note(temp_vault):
    manager = NoteManager()
    title = "Test Note"
    content = "This is a test note."
    tags = ["test", "example"]

    manager.create_note(title, content, tags)

    note = manager.get_note(title)
    assert note is not None
    assert note['title'] == title
    assert note.content.strip() == content
    assert set(note['tags']) == set(tags)

def test_update_note(temp_vault):
    manager = NoteManager()
    title = "Update Test"
    manager.create_note(title, "Initial content")

    new_content = "Updated content"
    new_tags = ["updated"]
    result = manager.update_note(title, new_content, new_tags)

    assert result is True
    updated_note = manager.get_note(title)
    assert updated_note.content.strip() == new_content
    assert set(updated_note['tags']) == set(new_tags)

def test_delete_note(temp_vault):
    manager = NoteManager()
    title = "Delete Test"
    manager.create_note(title)

    result = manager.delete_note(title)
    assert result is True

    deleted_note = manager.get_note(title)
    assert deleted_note is None
