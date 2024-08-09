import os
import shutil
from datetime import datetime
from ..obsidian_helper import load_config, get_all_files, get_file_content, write_to_file

def backup_vault():
    config = load_config()
    vault_path = config['obsidian']['vault_path']
    backup_path = os.path.join(config['obsidian']['backup_path'], f'backup-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}')
    shutil.copytree(vault_path, backup_path)
    print(f"Vault backed up to {backup_path}")

def export_notes_to_html(config):
    vault_path = config.get('obsidian', {}).get('vault_path')
    if not vault_path:
        raise ValueError("Vault path not found in configuration")
    
    export_path = os.path.join(vault_path, 'Exports', f'export-{datetime.now().strftime("%Y-%m-%d-%H%M%S")}')
    os.makedirs(export_path, exist_ok=True)

    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            content = get_file_content(file_path)
            html_content = markdown_to_html(content)
            html_file_path = os.path.join(export_path, os.path.splitext(os.path.basename(file_path))[0] + '.html')
            write_to_file(html_file_path, html_content)

    print(f"Notes exported to HTML in {export_path}")
    return export_path

def markdown_to_html(markdown_text):
    from markdown2 import markdown
    return markdown(markdown_text)

if __name__ == "__main__":
    config = load_config()
    backup_vault(config)
    export_notes_to_html(config)
