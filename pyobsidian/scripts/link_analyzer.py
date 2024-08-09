from ..obsidian_helper import get_all_files, get_file_content, write_to_file
import os
import re
from collections import defaultdict

def analyze_links(config):
    vault_path = config['vault_path']
    analysis_file = os.path.join(vault_path, 'link_analysis.md')
    
    incoming_links = defaultdict(list)
    outgoing_links = defaultdict(list)
    
    for file_path in get_all_files(vault_path):
        content = get_file_content(file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        relative_path = os.path.relpath(file_path, vault_path)
        
        links = re.findall(r'\[\[(.+?)\]\]', content)
        for link in links:
            outgoing_links[file_name].append(link)
            incoming_links[link].append(file_name)
    
    analysis_content = "# Link Analysis\n\n"
    
    analysis_content += "## Most Linked Notes\n\n"
    for note, links in sorted(incoming_links.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        analysis_content += f"- {note}: {len(links)} incoming links\n"
    
    analysis_content += "\n## Notes with Most Outgoing Links\n\n"
    for note, links in sorted(outgoing_links.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        analysis_content += f"- {note}: {len(links)} outgoing links\n"
    
    write_to_file(analysis_file, analysis_content)
    return analysis_file
