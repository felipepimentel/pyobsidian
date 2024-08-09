import os
from textblob import TextBlob
from ..obsidian_helper import load_config, get_all_files, get_file_content, write_to_file

def analyze_content(config):
    vault_path = config['obsidian']['vault_path']
    sentiment_report = ""

    for file_path in get_all_files(vault_path):
        if file_path.endswith('.md'):
            content = get_file_content(file_path)
            blob = TextBlob(content)
            sentiment = blob.sentiment
            sentiment_report += f"File: {file_path}\n"
            sentiment_report += f"  Polarity: {sentiment.polarity}\n"
            sentiment_report += f"  Subjectivity: {sentiment.subjectivity}\n\n"

    report_path = os.path.join(vault_path, 'Reports', 'sentiment-analysis-report.md')
    write_to_file(report_path, sentiment_report)

if __name__ == "__main__":
    config = load_config()
    analyze_content(config)
    print("Sentiment analysis completed successfully.")
