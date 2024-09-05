import openai
from ..obsidian_helper import load_config, get_all_files, get_file_content, write_to_file
import os
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def setup_openai():
    config = load_config()
    openai.api_key = config['openai']['api_key']

def generate_insight(prompt, max_tokens=500):
    setup_openai()
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant specialized in analyzing knowledge bases and generating insights."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens
    )
    return response.choices[0].message['content'].strip()

def build_knowledge_graph(config):
    vault_path = config['obsidian']['vault_path']
    G = nx.Graph()
    notes = {}

    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            file_name = os.path.basename(file_path)[:-3]
            content = get_file_content(file_path)
            notes[file_name] = content
            G.add_node(file_name)

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(notes.values())
    
    for i, (note1, content1) in enumerate(notes.items()):
        for j, (note2, content2) in enumerate(notes.items()):
            if i < j:
                similarity = cosine_similarity(tfidf_matrix[i:i+1], tfidf_matrix[j:j+1])[0][0]
                if similarity > 0.2:  # Threshold for connection
                    G.add_edge(note1, note2, weight=similarity)

    return G, notes

def generate_ai_insights(config):
    G, notes = build_knowledge_graph(config)
    
    # Identify central nodes
    centrality = nx.eigenvector_centrality(G)
    central_nodes = sorted(centrality, key=centrality.get, reverse=True)[:5]
    
    # Identify clusters
    clusters = list(nx.community.greedy_modularity_communities(G))
    
    # Generate insights
    insights = []
    
    # Insight on central topics
    central_topics_prompt = f"The most central topics in the knowledge base are: {', '.join(central_nodes)}. Provide insights on why these topics might be important and how they relate to each other."
    insights.append(generate_insight(central_topics_prompt))
    
    # Insight on clusters
    for i, cluster in enumerate(clusters[:3]):  # Analyze top 3 clusters
        cluster_notes = [notes[node] for node in cluster]
        cluster_content = "\n\n".join(cluster_notes)
        cluster_prompt = f"Analyze the following group of related notes and provide insights on their common themes and potential areas for further exploration:\n\n{cluster_content[:2000]}"
        insights.append(generate_insight(cluster_prompt))
    
    # Identify potential gaps
    all_content = "\n\n".join(notes.values())
    gaps_prompt = f"Based on the following content from a knowledge base, identify potential gaps or areas that could benefit from further research:\n\n{all_content[:5000]}"
    insights.append(generate_insight(gaps_prompt))
    
    # Compile insights
    insight_content = "# AI-Generated Insights\n\n"
    for i, insight in enumerate(insights):
        insight_content += f"## Insight {i+1}\n\n{insight}\n\n"
    
    insight_path = os.path.join(config['obsidian']['vault_path'], 'ai_insights.md')
    write_to_file(insight_path, insight_content)
    return insight_path

if __name__ == "__main__":
    config = load_config()
    insight_path = generate_ai_insights(config)
    print(f"AI insights generated: {insight_path}")