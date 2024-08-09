import os
import matplotlib.pyplot as plt
from datetime import datetime
from ..obsidian_helper import load_config, get_all_files, get_file_content

def visualize_data(config):
    vault_path = config['obsidian']['vault_path']
    creation_dates = []

    for file_path in get_all_files(vault_path):
        creation_date = datetime.fromtimestamp(os.path.getctime(file_path))
        creation_dates.append(creation_date)

    creation_dates.sort()
    dates = [date.strftime("%Y-%m") for date in creation_dates]
    date_counts = {date: dates.count(date) for date in set(dates)}

    plt.bar(date_counts.keys(), date_counts.values())
    plt.xticks(rotation=90)
    plt.xlabel('Date')
    plt.ylabel('Number of Notes')
    plt.title('Notes Created Over Time')
    plt.show()

if __name__ == "__main__":
    config = load_config()
    visualize_data(config)
