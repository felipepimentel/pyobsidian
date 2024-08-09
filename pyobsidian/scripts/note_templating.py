from ..obsidian_helper import write_to_file
import os
import yaml

def create_note_from_template(config, template_name, note_name):
    vault_path = config['vault_path']
    templates_folder = os.path.join(vault_path, 'Templates')
    template_path = os.path.join(templates_folder, f"{template_name}.md")
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template {template_name} not found.")
    
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()
    
    # Replace placeholders in the template
    replacements = {
        '{{title}}': note_name,
        '{{date}}': '{{date:YYYY-MM-DD}}',
        '{{time}}': '{{time:HH:mm}}'
    }
    for placeholder, value in replacements.items():
        template_content = template_content.replace(placeholder, value)
    
    new_note_path = os.path.join(vault_path, f"{note_name}.md")
    write_to_file(new_note_path, template_content)
    return new_note_path

def list_templates(config):
    vault_path = config['vault_path']
    templates_folder = os.path.join(vault_path, 'Templates')
    
    if not os.path.exists(templates_folder):
        return []
    
    return [os.path.splitext(f)[0] for f in os.listdir(templates_folder) if f.endswith('.md')]
