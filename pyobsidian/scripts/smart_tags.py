from ..obsidian_helper import load_config, get_file_content, update_frontmatter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')

def extract_keywords(text, num_keywords=5):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())
    filtered_words = [word for word in word_tokens if word.isalnum() and word not in stop_words]
    word_freq = Counter(filtered_words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def suggest_smart_tags(note_path):
    content = get_file_content(note_path)
    keywords = extract_keywords(content)
    return keywords

def apply_smart_tags(config):
    vault_path = config['obsidian']['vault_path']
    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            suggested_tags = suggest_smart_tags(file_path)
            content = get_file_content(file_path)
            new_frontmatter = {'smart_tags': suggested_tags}
            new_content = update_frontmatter(content, new_frontmatter)
            write_to_file(file_path, new_content)
    return "Smart tags applied to all notes"

if __name__ == "__main__":
    config = load_config()
    apply_smart_tags(config)