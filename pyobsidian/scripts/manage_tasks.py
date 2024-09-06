from ..obsidian_helper import load_config, get_all_files, get_file_content, write_to_file
from collections import defaultdict
import os
from datetime import datetime
import re

def manage_tasks(config):
    vault_path = config['obsidian']['vault_path']
    tasks_folder = os.path.join(vault_path, 'Tasks')
    os.makedirs(tasks_folder, exist_ok=True)  # Ensure the Tasks folder exists
    task_pattern = re.compile(r'- \[ \] (.*)')
    task_notes = defaultdict(list)

    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            content = get_file_content(file_path)
            for task in task_pattern.findall(content):
                task_notes[task].append(file_path)

    task_summary = "# Task Summary\n\n"
    for task, files in task_notes.items():
        task_summary += f"- [ ] {task} (Found in: {', '.join(files)})\n"

    task_summary_path = os.path.join(tasks_folder, f'tasks-summary-{datetime.now().strftime("%Y-%m-%d")}.md')
    write_to_file(task_summary_path, task_summary)
    return task_summary_path

if __name__ == "__main__":
    config = load_config()
    task_summary_path = manage_tasks(config)
    print(f"Tasks summarized successfully. Summary file: {task_summary_path}")
