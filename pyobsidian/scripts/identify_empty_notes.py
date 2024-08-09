import os
from ..obsidian_helper import load_config, get_all_files, get_file_content

def identify_small_notes(config):
    vault_path = config['obsidian']['vault_path']
    small_note_threshold = config['obsidian']['small_note_threshold']
    empty_note_threshold = config['obsidian']['empty_note_threshold']

    small_notes = []
    empty_notes = []

    for file_path in get_all_files(vault_path):
        content = get_file_content(file_path)
        if len(content) < empty_note_threshold:
            empty_notes.append(file_path)
        elif len(content) < small_note_threshold:
            small_notes.append(file_path)

    return small_notes, empty_notes

if __name__ == "__main__":
    config = load_config()
    small_notes, empty_notes = identify_small_notes(config)

    print("Empty Notes:")
    for note in empty_notes:
        print(note)

    print("\nSmall Notes:")
    for note in small_notes:
        print(note)
