import os
import yaml
import re

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def get_all_files(vault_path, extension=".md"):
    for root, dirs, files in os.walk(vault_path):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)

def get_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_to_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def get_frontmatter(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return {}

def update_frontmatter(content, new_frontmatter):
    frontmatter = get_frontmatter(content)
    frontmatter.update(new_frontmatter)
    
    yaml_frontmatter = yaml.dump(frontmatter, default_flow_style=False)
    new_content = re.sub(r'^---\s*\n.*?\n---\s*\n', f'---\n{yaml_frontmatter}---\n', content, flags=re.DOTALL)
    
    if new_content == content:  # No frontmatter found, add it
        new_content = f'---\n{yaml_frontmatter}---\n\n{content}'
    
    return new_content
