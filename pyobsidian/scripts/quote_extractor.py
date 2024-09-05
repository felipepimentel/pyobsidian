from ..obsidian_helper import load_config, get_all_files, get_file_content, write_to_file
import re

def extract_quotes(config):
    vault_path = config['obsidian']['vault_path']
    quotes = []

    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            content = get_file_content(file_path)
            file_quotes = re.findall(r'> (.+)', content)
            for quote in file_quotes:
                quotes.append((quote, file_path))

    return quotes

def generate_quote_summary(config):
    quotes = extract_quotes(config)
    summary_content = "# Quote Summary\n\n"

    for quote, file_path in quotes:
        summary_content += f"- \"{quote}\" - [{os.path.basename(file_path)}]({file_path})\n"

    summary_path = os.path.join(config['obsidian']['vault_path'], 'quote_summary.md')
    write_to_file(summary_path, summary_content)
    return summary_path

if __name__ == "__main__":
    config = load_config()
    summary_path = generate_quote_summary(config)
    print(f"Quote summary generated: {summary_path}")