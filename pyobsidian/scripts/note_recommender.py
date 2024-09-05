from ..obsidian_helper import load_config, get_all_files, get_file_content
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def build_tfidf_matrix(config):
    vault_path = config['obsidian']['vault_path']
    notes = []
    file_paths = []
    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            content = get_file_content(file_path)
            notes.append(content)
            file_paths.append(file_path)
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(notes)
    return tfidf_matrix, file_paths

def get_related_notes(config, note_path, num_recommendations=5):
    tfidf_matrix, file_paths = build_tfidf_matrix(config)
    note_index = file_paths.index(note_path)
    note_vector = tfidf_matrix[note_index]
    
    cosine_similarities = cosine_similarity(note_vector, tfidf_matrix).flatten()
    related_indices = cosine_similarities.argsort()[:-num_recommendations-1:-1]
    
    related_notes = [file_paths[i] for i in related_indices if i != note_index]
    return related_notes

if __name__ == "__main__":
    config = load_config()
    test_note = config['obsidian']['vault_path'] + '/test_note.md'
    related_notes = get_related_notes(config, test_note)
    print(f"Notes related to {test_note}:")
    for note in related_notes:
        print(note)