# PyObsidian

PyObsidian is a powerful command-line tool for managing and analyzing Obsidian vaults. It provides a wide range of features to enhance your note-taking experience and optimize your knowledge management workflow.

![PyObsidian Logo](https://example.com/pyobsidian-logo.png)

[![Python Version](https://img.shields.io/pypi/pyversions/pyobsidian.svg)](https://pypi.org/project/pyobsidian/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/felipepimentel/pyobsidian.svg)](https://github.com/felipepimentel/pyobsidian/issues)
[![GitHub stars](https://img.shields.io/github/stars/felipepimentel/pyobsidian.svg)](https://github.com/felipepimentel/pyobsidian/stargazers)

## Features

- Create and manage notes
- Search notes by content, tags, and frontmatter
- Analyze notes (find empty notes, duplicates, unused images)
- Manage tags and generate tag clouds
- Create daily notes
- Backup and restore vaults
- Analyze links (find broken links and orphaned notes)
- Generate note statistics
- Google Calendar integration
- Voice note to text conversion
- Git synchronization
- Report generation
- Data visualization
- Tag management
- Link analysis
- Note templating
- Plugin management
- Spaced repetition
- Citation extraction
- Knowledge mapping

## Installation

1. Ensure you have Python 3.12.3 or later installed on your system.
2. Install Poetry if you haven't already:

   ```bash
   pip install poetry
   ```

3. Clone this repository:

   ```bash
   git clone https://github.com/felipepimentel/pyobsidian.git
   cd pyobsidian
   ```

4. Install project dependencies:

   ```bash
   poetry install
   ```

## Configuration

1. Create a `.env` file in the project root directory.
2. Add the following line to the `.env` file, replacing `/path/to/your/obsidian/vault` with the actual path to your Obsidian vault:

```bash
OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"
```

Note: The `.env` file is gitignored to keep your personal configuration private.

## Usage

To use PyObsidian, run the `pyobsidian` command followed by a subcommand. Here are some examples:

```bash
# Create a new note
poetry run pyobsidian create-note "My New Note" --content "This is the content" --tags "tag1,tag2"

# Search notes
poetry run pyobsidian search "query"

# List all tags
poetry run pyobsidian list-tags

# Create a backup
poetry run pyobsidian backup --destination "./my_backup"

# Find empty notes
poetry run pyobsidian find-empty-notes

# Create a daily note
poetry run pyobsidian create-daily-note

# Show top tags
poetry run pyobsidian top-tags --limit 5

# Sync with Git
poetry run pyobsidian sync-git

# Process voice notes
poetry run pyobsidian process-voice-notes

# Generate report
poetry run pyobsidian generate-report

# Manage tags
poetry run pyobsidian manage-tags

# Analyze links
poetry run pyobsidian analyze-links

# Create note from template
poetry run pyobsidian create-note "Template Name" "New Note Name"

# List available templates
poetry run pyobsidian list-templates

# Check for plugin updates
poetry run pyobsidian check-plugin-updates
```

For a complete list of available commands, run:

```bash
poetry run pyobsidian --help
```

## Development

To set up the development environment:

1. Install development dependencies:

   ```bash
   poetry install
   ```

2. Run tests:

   ```bash
   poetry run pytest
   ```

3. Format code:

   ```bash
   poetry run black .
   ```

4. Run linter:

   ```bash
   poetry run flake8
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Felipe Pimentel - [@felipepimentel](https://twitter.com/felipepimentel)

Project Link: [https://github.com/felipepimentel/pyobsidian](https://github.com/felipepimentel/pyobsidian)

## Acknowledgements

- [Obsidian](https://obsidian.md/) for providing an excellent note-taking tool
- All contributors who have dedicated time to improve this project

## Documentation for Developers

### Project Structure

```
pyobsidian/
├── pyobsidian/
│   ├── __init__.py
│   ├── cli.py
│   ├── obsidian_helper.py
│   └── scripts/
│       ├── analyze_content.py
│       ├── archive_old_notes.py
│       ├── backup_and_export.py
│       ├── daily_note_generator.py
│       ├── extract_citations.py
│       ├── generate_index.py
│       ├── generate_reports.py
│       ├── google_calendar_integration.py
│       ├── identify_broken_links.py
│       ├── identify_duplicate_notes.py
│       ├── identify_empty_notes.py
│       ├── identify_unused_images.py
│       ├── incremental_backup.py
│       ├── knowledge_map.py
│       ├── link_analyzer.py
│       ├── manage_tasks.py
│       ├── merge_agenda_notes.py
│       ├── note_templating.py
│       ├── notify.py
│       ├── plugin_manager.py
│       ├── spaced_repetition.py
│       ├── sync_with_git.py
│       ├── tag_management.py
│       ├── visualize_data.py
│       └── voice_notes.py
├── tests/
│   ├── test_backup.py
│   ├── test_note_manager.py
│   ├── test_search.py
│   └── test_tag_manager.py
├── .gitignore
├── LICENSE
├── poetry.lock
├── pyproject.toml
└── README.md
```

### Key Components

1. **cli.py**: Contains the main command-line interface using Click.
2. **obsidian_helper.py**: Provides utility functions for interacting with Obsidian vaults.
3. **scripts/**: Contains individual script files for each feature.

### Adding a New Feature

To add a new feature:

1. Create a new script file in the `scripts/` directory.
2. Implement the main functionality in the new script.
3. Add a new command in `cli.py` to expose the functionality.
4. Update the README.md with the new command and its description.
5. Add tests for the new feature in the `tests/` directory.

### Coding Standards

- Follow PEP 8 guidelines for Python code style.
- Use type hints where appropriate.
- Write docstrings for all functions and classes.
- Maintain test coverage for new features.

### Testing

We use pytest for testing. To run tests:

```bash
poetry run pytest
```

### Continuous Integration

We use GitHub Actions for CI/CD. The workflow is defined in `.github/workflows/main.yml`.

### Versioning

We use Semantic Versioning (SemVer) for version numbers. Update the version in `pyproject.toml` when making releases.

### Documentation

- Keep this README.md up to date with new features and changes.
- Use inline comments for complex logic.
- Consider adding a more comprehensive documentation using Sphinx for larger features.

For more detailed information on each module and function, please refer to the inline documentation in the source code.
