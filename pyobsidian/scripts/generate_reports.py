import os
from datetime import datetime
from ..obsidian_helper import load_config, get_all_files, get_file_content, write_to_file
from .identify_empty_notes import identify_small_notes
from .identify_unused_images import identify_unused_images
from .identify_duplicate_notes import identify_duplicate_notes
from .identify_broken_links import identify_broken_links
from .manage_tasks import manage_tasks

def generate_report(config):
    vault_path = config['obsidian']['vault_path']
    report_folder = os.path.join(vault_path, 'Reports')
    os.makedirs(report_folder, exist_ok=True)
    
    report_content = f"# Obsidian Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Empty and Small Notes
    small_notes, empty_notes = identify_small_notes(config)
    report_content += "## Empty Notes\n"
    for note in empty_notes:
        report_content += f"- {note}\n"
    
    report_content += "\n## Small Notes\n"
    for note in small_notes:
        report_content += f"- {note}\n"
    
    # Unused Images
    unused_images = identify_unused_images(config)
    report_content += "\n## Unused Images\n"
    for image in unused_images:
        report_content += f"- {image}\n"
    
    # Duplicate Notes
    duplicates = identify_duplicate_notes(config)
    report_content += "\n## Duplicate Notes\n"
    for content, files in duplicates.items():
        report_content += f"\n### Content: {content[:100]}...\n"
        for file in files:
            report_content += f"- {file}\n"
    
    # Broken Links
    broken_links = identify_broken_links(config)
    report_content += "\n## Broken Links\n"
    for file, links in broken_links.items():
        report_content += f"\n### File: {file}\n"
        for link in links:
            report_content += f"- Broken Link: {link}\n"
    
    # Task Summary
    task_summary_path = os.path.join(report_folder, 'task-summary.md')
    manage_tasks(config)
    if os.path.exists(task_summary_path):
        with open(task_summary_path, 'r') as task_file:
            report_content += "\n## Task Summary\n"
            report_content += task_file.read()
    else:
        report_content += "\n## Task Summary\n"
        report_content += "Nenhum resumo de tarefas disponível.\n"

    report_path = os.path.join(report_folder, f'report-{datetime.now().strftime("%Y-%m-%d-%H%M%S")}.md')
    write_to_file(report_path, report_content)

if __name__ == "__main__":
    config = load_config()
    generate_report(config)
    print("Report generated successfully.")
