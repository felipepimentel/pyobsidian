import os
import shutil
from datetime import datetime, timedelta
from ..obsidian_helper import load_config, get_all_files

def archive_old_notes(config):
    vault_path = config['obsidian']['vault_path']
    archive_path = os.path.join(vault_path, 'Archived')
    os.makedirs(archive_path, exist_ok=True)
    
    archive_days_threshold = config['obsidian'].get('archive_days_threshold', 180)
    threshold_date = datetime.now() - timedelta(days=archive_days_threshold)

    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mod_time < threshold_date:
                shutil.move(file_path, archive_path)

if __name__ == "__main__":
    config = load_config()
    archive_old_notes(config)
    print("Old notes archived successfully.")
