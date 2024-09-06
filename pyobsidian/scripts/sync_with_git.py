from ..obsidian_helper import load_config
import os
import subprocess
from datetime import datetime

def sync_with_git(config):
    vault_path = config['obsidian']['vault_path']
    commit_message = f"Automated commit on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    try:
        subprocess.run(["git", "add", "."], cwd=vault_path, check=True)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=vault_path, check=True)
        subprocess.run(["git", "push"], cwd=vault_path, check=True)
        print("Changes pushed to Git repository successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while syncing with Git: {e}")

if __name__ == "__main__":
    config = load_config()
    sync_with_git(config)
