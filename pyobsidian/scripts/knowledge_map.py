from ..obsidian_helper import get_all_files, get_file_content, write_to_file
import os
import re
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

def create_knowledge_map(config):
    vault_path = config['vault_path']
    map_file = os.path.join(vault_path, 'knowledge_map.png')
    
    G = nx.Graph()
    
    # Count the number of links for each note
    link_count = Counter()
    
    for file_path in get_all_files(vault_path):
        content = get_file_content(file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        G.add_node(file_name)
        
        links = re.findall(r'\[\[(.+?)\]\]', content)
        for link in links:
            G.add_edge(file_name, link)
            link_count[file_name] += 1
            link_count[link] += 1
    
    plt.figure(figsize=(30, 30))
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    # Normalize node sizes based on link count
    max_count = max(link_count.values())
    node_sizes = [1000 + 5000 * (count / max_count) for node, count in link_count.items()]
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=node_sizes, font_size=8, font_weight='bold')
    
    # Add edge labels (number of connections)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.savefig(map_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return map_file
