import pytest
import os
import tempfile
from pyobsidian.backup import Backup
from pyobsidian.note_manager import NoteManager

@pytest.fixture
def temp_vault():
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.environ['OBSIDIAN_VAULT_PATH'] = tmpdirname
        yield tmpdirname

@pytest.fixture
def temp_backup_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_create_backup(temp_vault, temp_backup_dir):
    note_manager = NoteManager()
    note_manager.create_note("Test Note", "This is a test note.")

    backup = Backup()
    backup_path = backup.create_backup(temp_backup_dir)

    assert backup_path is not None
    assert os.path.exists(backup_path)
    assert os.path.exists(os.path.join(backup_path, "Test Note.md"))

def test_restore_backup(temp_vault, temp_backup_dir):
    note_manager = NoteManager()
    note_manager.create_note("Original Note", "This is the original note.")

    backup = Backup()
    backup_path = backup.create_backup(temp_backup_dir)

    # Modificar o vault original
    note_manager.create_note("New Note", "This is a new note.")
    note_manager.delete_note("Original Note")

    # Restaurar o backup
    result = backup.restore_backup(backup_path)

    assert result is True
    assert os.path.exists(os.path.join(temp_vault, "Original Note.md"))
    assert not os.path.exists(os.path.join(temp_vault, "New Note.md"))
