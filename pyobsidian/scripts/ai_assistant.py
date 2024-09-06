import openai
from ..obsidian_helper import load_config, get_all_files, get_file_content, write_to_file
import os

def setup_openai(config):
    openai.api_key = config['openai']['api_key']

def generate_content(config, prompt, max_tokens=500):
    setup_openai(config)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant helping with note-taking and knowledge management."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens
    )
    return response.choices[0].message['content'].strip()

def enhance_note(config, note_path):
    content = get_file_content(note_path)
    prompt = f"Enhance the following note with additional insights, connections to other topics, and potential areas for further exploration:\n\n{content}"
    enhanced_content = generate_content(config, prompt, max_tokens=1000)
    
    new_content = f"{content}\n\n## AI-Enhanced Content\n\n{enhanced_content}"
    write_to_file(note_path, new_content)
    return note_path

def generate_note_ideas(config, topic):
    prompt = f"Generate 5 detailed note ideas related to the topic: {topic}. For each idea, provide a brief outline of potential subtopics to cover."
    ideas = generate_content(config, prompt)
    return ideas

def analyze_vault(config):
    vault_path = config['obsidian']['vault_path']
    all_content = ""
    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            all_content += get_file_content(file_path) + "\n\n"
    
    prompt = f"Analyze the following content from a knowledge vault and provide insights on main themes, potential knowledge gaps, and suggestions for new areas of study:\n\n{all_content[:5000]}"  # Limiting to first 5000 characters for API constraints
    analysis = generate_content(config, prompt, max_tokens=1500)
    
    analysis_path = os.path.join(vault_path, 'vault_analysis.md')
    write_to_file(analysis_path, analysis)
    return analysis_path

if __name__ == "__main__":
    config = load_config()
    note_path = os.path.join(config['obsidian']['vault_path'], 'test_note.md')
    enhanced_note = enhance_note(config, note_path)
    print(f"Enhanced note: {enhanced_note}")
    print(generate_note_ideas(config, "productivity"))
    analysis_path = analyze_vault(config)
    print(f"Vault analysis: {analysis_path}")