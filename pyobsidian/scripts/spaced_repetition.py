from ..obsidian_helper import load_config, get_all_files, get_file_content, write_to_file, update_frontmatter
from datetime import datetime, timedelta

def calculate_next_review_date(current_interval):
    if current_interval == 0:
        return 1
    elif current_interval == 1:
        return 3
    else:
        return current_interval * 2

def update_review_dates(config):
    vault_path = config['obsidian']['vault_path']
    today = datetime.now().date()
    notes_to_review = []

    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            content = get_file_content(file_path)
            frontmatter = get_frontmatter(content)
            
            if 'review_date' in frontmatter:
                review_date = datetime.strptime(frontmatter['review_date'], '%Y-%m-%d').date()
                if review_date <= today:
                    notes_to_review.append(file_path)
                    current_interval = frontmatter.get('review_interval', 0)
                    new_interval = calculate_next_review_date(current_interval)
                    new_review_date = today + timedelta(days=new_interval)
                    
                    new_frontmatter = {
                        'review_date': new_review_date.strftime('%Y-%m-%d'),
                        'review_interval': new_interval
                    }
                    new_content = update_frontmatter(content, new_frontmatter)
                    write_to_file(file_path, new_content)

    return notes_to_review

if __name__ == "__main__":
    config = load_config()
    notes_to_review = update_review_dates(config)
    print(f"Notes to review today: {len(notes_to_review)}")
    for note in notes_to_review:
        print(note)
