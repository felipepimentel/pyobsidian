from ..obsidian_helper import load_config, get_all_files
import os
import shutil
from datetime import datetime

def incremental_backup(config):
    vault_path = config['obsidian']['vault_path']
    backup_path = config['obsidian']['backup_path']
    os.makedirs(backup_path, exist_ok=True)

    last_backup_file = os.path.join(backup_path, 'last_backup.txt')
    last_backup_time = None

    if os.path.exists(last_backup_file):
        with open(last_backup_file, 'r') as file:
            last_backup_time = datetime.strptime(file.read().strip(), '%Y-%m-%d %H:%M:%S')

    current_time = datetime.now()
    current_backup_folder = os.path.join(backup_path, current_time.strftime('%Y-%m-%d_%H-%M-%S'))
    os.makedirs(current_backup_folder, exist_ok=True)

    for file_path in get_all_files(vault_path):
        if not file_path.startswith(backup_path):
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if last_backup_time is None or mod_time > last_backup_time:
                rel_path = os.path.relpath(file_path, vault_path)
                backup_file_path = os.path.join(current_backup_folder, rel_path)
                os.makedirs(os.path.dirname(backup_file_path), exist_ok=True)
                shutil.copy2(file_path, backup_file_path)

    with open(last_backup_file, 'w') as file:
        file.write(current_time.strftime('%Y-%m-%d %H:%M:%S'))

    return current_backup_folder

if __name__ == "__main__":
    config = load_config()
    backup_folder = incremental_backup(config)
    print(f"Incremental backup completed successfully. Backup folder: {backup_folder}")
