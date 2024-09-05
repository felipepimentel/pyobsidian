import dropbox
from ..obsidian_helper import load_config, get_all_files
import os

def setup_dropbox():
    config = load_config()
    return dropbox.Dropbox(config['dropbox']['access_token'])

def sync_to_dropbox(config):
    dbx = setup_dropbox()
    vault_path = config['obsidian']['vault_path']

    for file_path in get_all_files(vault_path):
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        relative_path = os.path.relpath(file_path, vault_path)
        dropbox_path = f"/ObsidianVault/{relative_path}"

        try:
            dbx.files_upload(file_data, dropbox_path, mode=dropbox.files.WriteMode.overwrite)
        except Exception as e:
            print(f"Error uploading {file_path}: {e}")

    return "Sync to Dropbox completed"

if __name__ == "__main__":
    config = load_config()
    sync_to_dropbox(config)