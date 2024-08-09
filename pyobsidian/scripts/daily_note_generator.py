from ..obsidian_helper import write_to_file
import os
from datetime import datetime

def generate_daily_note(config):
    vault_path = config['vault_path']
    daily_notes_folder = os.path.join(vault_path, 'Daily Notes')
    
    if not os.path.exists(daily_notes_folder):
        os.makedirs(daily_notes_folder)
    
    today = datetime.now()
    file_name = today.strftime("%Y-%m-%d.md")
    file_path = os.path.join(daily_notes_folder, file_name)
    
    content = f"""# {today.strftime("%Y-%m-%d")}

## Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Notes

## Journal

"""
    
    write_to_file(file_path, content)
    return file_path
