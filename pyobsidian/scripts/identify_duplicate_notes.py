import os
from collections import defaultdict
from ..obsidian import load_config, get_all_files, get_file_content

def identify_duplicate_notes(config):
    vault_path = config['obsidian']['vault_path']
    content_map = defaultdict(list)

    for file_path in get_all_files(vault_path):
        content = get_file_content(file_path)
        content_map[content.strip()].append(file_path)

    duplicates = {content: files for content, files in content_map.items() if len(files) > 1}
    return duplicates

if __name__ == "__main__":
    config = load_config()
    duplicates = identify_duplicate_notes(config)

    print("Duplicate Notes:")
    for content, files in duplicates.items():
        print(f"\nContent: {content[:100]}...")  # Print a snippet of the content
        for file in files:
            print(f"  {file}")
