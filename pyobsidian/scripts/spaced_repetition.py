from ..obsidian_helper import get_all_files, get_file_content, write_to_file, update_frontmatter, get_frontmatter
import os
from datetime import datetime, timedelta

def spaced_repetition(config):
    vault_path = config['vault_path']
    review_file = os.path.join(vault_path, 'review.md')
    
    review_content = "# Spaced Repetition Review\n\n"
    today = datetime.now().date()
    
    for file_path in get_all_files(vault_path):
        content = get_file_content(file_path)
        frontmatter = get_frontmatter(content)
        
        if 'review_date' in frontmatter:
            review_date = datetime.strptime(frontmatter['review_date'], '%Y-%m-%d').date()
            if review_date <= today:
                file_name = os.path.splitext(os.path.basename(file_path))[0]
                relative_path = os.path.relpath(file_path, vault_path)
                review_content += f"- [{file_name}]({relative_path})\n"
                
                # Update review date using spaced repetition algorithm
                days_since_last_review = (today - review_date).days
                new_interval = max(1, int(days_since_last_review * 1.5))  # Increase interval by 50%
                new_review_date = today + timedelta(days=new_interval)
                
                new_frontmatter = {'review_date': new_review_date.strftime('%Y-%m-%d')}
                new_content = update_frontmatter(content, new_frontmatter)
                write_to_file(file_path, new_content)
    
    write_to_file(review_file, review_content)
    return review_file
