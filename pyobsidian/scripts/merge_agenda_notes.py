import os
import yaml
from datetime import datetime
from ..obsidian_helper import load_config, get_all_files, get_file_content, write_to_file

def read_frontmatter(content):
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            frontmatter = yaml.safe_load(content[3:end])
            body = content[end+3:].strip()
            return frontmatter, body
    return {}, content

def merge_agenda_notes(config):
    vault_path = config['obsidian']['vault_path']
    agenda_prefix = config['obsidian']['agenda_prefix']
    merged_notes_folder = os.path.join(vault_path, config['obsidian']['merged_notes_folder'])
    os.makedirs(merged_notes_folder, exist_ok=True)

    merged_content = ""
    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            content = get_file_content(file_path)
            frontmatter, body = read_frontmatter(content)

            if os.path.basename(file_path).startswith(agenda_prefix) or frontmatter.get('type') == 'agenda':
                merged_content += f"# {os.path.basename(file_path)}\n\n{body}\n\n"

    merged_note_path = os.path.join(merged_notes_folder, f"merged-1on1-{datetime.now().strftime('%Y-%m-%d')}.md")
    write_to_file(merged_note_path, merged_content)

if __name__ == "__main__":
    config = load_config()
    merge_agenda_notes(config)
    print("Agenda notes merged successfully.")
