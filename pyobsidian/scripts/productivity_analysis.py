from ..obsidian_helper import load_config, get_all_files, get_file_content
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def analyze_productivity(config, days=30):
    vault_path = config['obsidian']['vault_path']
    today = datetime.now().date()
    start_date = today - timedelta(days=days)

    daily_activity = {(start_date + timedelta(days=i)).strftime('%Y-%m-%d'): 0 for i in range(days)}

    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).date()
            if start_date <= mod_time <= today:
                daily_activity[mod_time.strftime('%Y-%m-%d')] += 1

    dates = list(daily_activity.keys())
    activity = list(daily_activity.values())

    plt.figure(figsize=(15, 5))
    plt.bar(dates, activity)
    plt.xlabel('Date')
    plt.ylabel('Number of Notes Modified')
    plt.title(f'Productivity Analysis (Last {days} Days)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = os.path.join(vault_path, 'productivity_analysis.png')
    plt.savefig(output_path)
    plt.close()

    return output_path

if __name__ == "__main__":
    config = load_config()
    output_path = analyze_productivity(config)
    print(f"Productivity analysis generated: {output_path}")