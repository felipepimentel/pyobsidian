from ..obsidian_helper import load_config, get_all_files, get_file_content
import networkx as nx
import matplotlib.pyplot as plt
import re

def extract_links(content):
    return re.findall(r'\[\[(.+?)\]\]', content)

def generate_knowledge_graph(config):
    vault_path = config['obsidian']['vault_path']
    G = nx.Graph()

    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            file_name = os.path.basename(file_path)[:-3]  # Remove .md extension
            content = get_file_content(file_path)
            links = extract_links(content)
            
            G.add_node(file_name)
            for link in links:
                G.add_edge(file_name, link)

    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=1500, font_size=8, font_weight='bold')
    
    output_path = os.path.join(vault_path, 'knowledge_graph.png')
    plt.savefig(output_path)
    plt.close()

    return output_path

if __name__ == "__main__":
    config = load_config()
    graph_path = generate_knowledge_graph(config)
    print(f"Knowledge graph generated: {graph_path}")