from ..obsidian_helper import load_config, get_all_files, get_file_content, write_to_file
import os
import re

def extract_citations(config):
    vault_path = config['obsidian']['vault_path']
    citations_file = os.path.join(vault_path, 'citations.md')
    
    citations_content = "# Extracted Citations\n\n"
    
    for file_path in get_all_files(vault_path):
        content = get_file_content(file_path)
        citations = re.findall(r'> (.+)', content)
        inline_citations = re.findall(r'\[(@\w+)\]', content)
        
        if citations or inline_citations:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            relative_path = os.path.relpath(file_path, vault_path)
            citations_content += f"## [{file_name}]({relative_path})\n\n"
            
            for citation in citations:
                citations_content += f"- {citation}\n"
            
            for citation in inline_citations:
                citations_content += f"- Citação inline: {citation}\n"
            
            citations_content += "\n"
    
    write_to_file(citations_file, citations_content)
    return citations_file

if __name__ == "__main__":
    config = load_config()
    citations_file = extract_citations(config)
    print(f"Citations extracted to: {citations_file}")
