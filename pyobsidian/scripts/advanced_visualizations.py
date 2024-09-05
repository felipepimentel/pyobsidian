import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from ..obsidian_helper import load_config, get_all_files, get_file_content, get_frontmatter
import seaborn as sns
import pandas as pd

def visualize_tag_evolution(config):
    vault_path = config['obsidian']['vault_path']
    tag_evolution = defaultdict(lambda: defaultdict(int))

    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            content = get_file_content(file_path)
            frontmatter = get_frontmatter(content)
            date = frontmatter.get('date') or datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d')
            tags = frontmatter.get('tags', [])
            
            for tag in tags:
                tag_evolution[tag][date] += 1

    plt.figure(figsize=(15, 10))
    for tag, dates in tag_evolution.items():
        dates = sorted(dates.items())
        plt.plot(*zip(*dates), label=tag)

    plt.xlabel('Date')
    plt.ylabel('Number of Notes')
    plt.title('Tag Evolution Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = os.path.join(vault_path, 'tag_evolution.png')
    plt.savefig(output_path)
    plt.close()
    return output_path

def visualize_note_length_distribution(config):
    vault_path = config['obsidian']['vault_path']
    note_data = []

    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            content = get_file_content(file_path)
            frontmatter = get_frontmatter(content)
            date = frontmatter.get('date') or datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d')
            note_length = len(content.split())
            note_data.append({'date': date, 'length': note_length})

    df = pd.DataFrame(note_data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    plt.figure(figsize=(15, 10))
    sns.scatterplot(data=df, x='date', y='length', alpha=0.6)
    sns.regplot(data=df, x='date', y='length', scatter=False, color='red')

    plt.xlabel('Date')
    plt.ylabel('Note Length (words)')
    plt.title('Note Length Distribution Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = os.path.join(vault_path, 'note_length_distribution.png')
    plt.savefig(output_path)
    plt.close()
    return output_path

if __name__ == "__main__":
    config = load_config()
    visualize_tag_evolution(config)