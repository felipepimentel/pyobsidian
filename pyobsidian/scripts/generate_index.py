from ..obsidian_helper import get_all_files, get_file_content, write_to_file
import os

def generate_index(config):
    vault_path = config['vault_path']
    index_file = os.path.join(vault_path, 'index.md')
    
    index_content = "# Notes Index\n\n"
    
    for file_path in get_all_files(vault_path):
        content = get_file_content(file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        relative_path = os.path.relpath(file_path, vault_path)
        
        # Extract the first heading as the note title
        title = file_name
        for line in content.split('\n'):
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        index_content += f"- [{title}]({relative_path})\n"
    
    write_to_file(index_file, index_content)
    return index_file
