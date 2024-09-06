from ..obsidian_helper import load_config, get_all_files, get_file_content, write_to_file
import os
import re
from collections import defaultdict

def manage_tags(config):
    vault_path = config['obsidian']['vault_path']
    tag_file = os.path.join(vault_path, 'tag_summary.md')
    
    tag_dict = defaultdict(list)
    
    for file_path in get_all_files(vault_path):
        content = get_file_content(file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        relative_path = os.path.relpath(file_path, vault_path)
        
        tags = re.findall(r'#(\w+)', content)
        for tag in tags:
            tag_dict[tag].append(f"[{file_name}]({relative_path})")
    
    tag_content = "# Tag Summary\n\n"
    for tag, files in sorted(tag_dict.items()):
        tag_content += f"## #{tag}\n\n"
        for file in files:
            tag_content += f"- {file}\n"
        tag_content += "\n"
    
    write_to_file(tag_file, tag_content)
    return tag_file

if __name__ == "__main__":
    config = load_config()
    tag_file = manage_tags(config)
    print(f"Tag summary generated: {tag_file}")
