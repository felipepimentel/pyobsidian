from ..obsidian_helper import load_config, get_all_files, get_file_content
import os

def identify_unused_images(config):
    vault_path = config['obsidian']['vault_path']
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    image_files = set(file for file in get_all_files(vault_path) if any(file.endswith(ext) for ext in image_extensions))
    used_images = set()

    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            content = get_file_content(file_path)
            for image in image_files:
                if os.path.basename(image) in content:
                    used_images.add(image)

    unused_images = image_files - used_images
    return unused_images

if __name__ == "__main__":
    config = load_config()
    unused_images = identify_unused_images(config)

    print("Unused Images:")
    for image in unused_images:
        print(image)
