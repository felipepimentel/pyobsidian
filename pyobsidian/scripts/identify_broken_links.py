import os
import re
from collections import defaultdict
from ..obsidian_helper import load_config, get_all_files, get_file_content

def identify_broken_links(config):
    vault_path = config['obsidian']['vault_path']
    md_files = {os.path.splitext(os.path.basename(file))[0]: file for file in get_all_files(vault_path)}
    broken_links = defaultdict(list)
    link_pattern = re.compile(r'\[\[([^\]]+)\]\]')

    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            content = get_file_content(file_path)
            for match in link_pattern.findall(content):
                link_name = match.split('|')[0]
                if link_name not in md_files:
                    broken_links[file_path].append(link_name)

    return broken_links

if __name__ == "__main__":
    config = load_config()
    broken_links = identify_broken_links(config)

    print("Broken Links:")
    for file, links in broken_links.items():
        print(f"\nFile: {file}")
        for link in links:
            print(f"  Broken Link: {link}")
