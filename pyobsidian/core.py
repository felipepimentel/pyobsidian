from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Pattern, Union

import yaml
import time


class ObsidianCliError(Exception):
    """Base exception for ObsidianCLI errors."""


class ConfigError(ObsidianCliError):
    """Raised when there's an error in the configuration."""


class FileOperationError(ObsidianCliError):
    """Raised when there's an error in file operations."""


class Config:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_data = self._load_config(config_path)
        self.vault_path: Optional[str] = self.config_data.get("obsidian", {}).get(
            "vault_path"
        )
        self.excluded_patterns: List[Pattern] = self._compile_exclusion_patterns(
            self.config_data.get("obsidian", {}).get("excluded_files", [])
        )

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load the configuration from the specified YAML file."""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                if not isinstance(config, dict) or "obsidian" not in config:
                    raise ConfigError(
                        "Invalid configuration structure. 'obsidian' key is missing."
                    )
                return config
        except FileNotFoundError:
            raise ConfigError(f"Config file not found: {config_path}")
        except yaml.YAMLError:
            raise ConfigError(f"Invalid YAML in config file: {config_path}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the configuration."""
        return self.config_data.get("obsidian", {}).get(key, default)

    def _compile_exclusion_patterns(self, patterns: List[str]) -> List[Pattern]:
        """Compile exclusion patterns from the configuration."""
        compiled_patterns = []
        for pattern in patterns:
            if pattern.startswith("**/") and pattern.endswith("/**"):
                regex = pattern.replace("**/", "(.*/)?").replace("/**", "(/.*)?")
                compiled_patterns.append(re.compile(regex))
            else:
                compiled_patterns.append(re.compile(pattern))
        return compiled_patterns


class Link:
    """A link between notes in the vault."""

    def __init__(self, source: Union[str, "Note"], target: str, alias: Optional[str] = None) -> None:
        """Initialize a link.
        
        Args:
            source: The source note or path.
            target: The target path.
            alias: Optional alias for the link.
        """
        self._source = source
        self._target = target.strip()  # Remove whitespace
        self._alias = alias.strip() if alias else None

    @property
    def source(self) -> Union[str, "Note"]:
        """Get the source note or path."""
        return self._source

    @property
    def target(self) -> str:
        """Get the target path."""
        return self._target.removesuffix('.md')  # Remove .md suffix if present

    @property
    def alias(self) -> Optional[str]:
        """Get the link alias."""
        return self._alias

    def __repr__(self) -> str:
        """Get a string representation of the link."""
        return f"Link(source={self.source}, target={self.target}, alias={self.alias})"

    def __eq__(self, other: object) -> bool:
        """Check if two links are equal."""
        if not isinstance(other, Link):
            return NotImplemented
        return (self.source == other.source and 
                self.target == other.target and 
                self.alias == other.alias)


class Note:
    """A note in the vault."""

    def __init__(self, path: str, content: str) -> None:
        """Initialize a note.
        
        Args:
            path: The path to the note file.
            content: The content of the note.
        """
        self._path = path
        self._content = content
        self._title = self._extract_title()
        self._links = self._extract_links()

    def _extract_title(self) -> str:
        """Extract the title from the note content."""
        if not self._content.strip():
            return ""
        lines = self._content.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        return ""  # Return empty string if no H1 header found

    @property
    def tags(self) -> List[str]:
        """Get all tags in the note content."""
        # Remove code blocks first
        content = self._remove_code_blocks(self._content)
        
        # Find all tags
        pattern = r'#([a-zA-Z0-9][\w-]*(?:-[\w-]+)*)'
        matches = re.finditer(pattern, content)
        
        # Keep track of seen tags to avoid duplicates
        seen = set()
        tags = []
        
        for match in matches:
            tag = match.group(1)
            # Skip invalid tags
            if tag.startswith('!') or tag.startswith('-') or tag.endswith('-'):
                continue
            if tag not in seen:
                seen.add(tag)
                tags.append(tag)
        
        return tags

    def _remove_code_blocks(self, content: str) -> str:
        """Remove fenced code blocks and inline code."""
        # Remove fenced code blocks
        content = re.sub(r'```[^`]*```', '', content, flags=re.DOTALL)
        # Remove inline code
        content = re.sub(r'`[^`]+`', '', content)
        return content

    def _remove_emphasis(self, content: str) -> str:
        """Remove emphasis markers and their content."""
        content = re.sub(r'\*\*[^*]+\*\*', '', content)  # Bold
        content = re.sub(r'\*[^*]+\*', '', content)      # Italic
        content = re.sub(r'__[^_]+__', '', content)      # Underline
        content = re.sub(r'_[^_]+_', '', content)        # Single underscore
        return content

    @property
    def word_count(self) -> int:
        """Calculate the number of words in the note content."""
        # Remove code blocks
        content = self._remove_code_blocks(self._content)
        
        # Remove links and tags
        content = re.sub(r'\[\[.*?\]\]', '', content)  # Remove links
        content = re.sub(r'#\w+', '', content)  # Remove tags
        
        # Remove headers
        content = re.sub(r'^#+\s.*$', '', content, flags=re.MULTILINE)
        
        # Remove emphasis markers
        content = re.sub(r'[*_`]', '', content)
        
        # Remove punctuation and normalize whitespace
        content = re.sub(r'[^\w\s]', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        
        # Split into words and count non-empty ones
        words = [word for word in content.split() if word.strip()]
        return len(words)

    def _extract_links(self) -> List[Link]:
        """Extract all links from the note content."""
        links = []
        
        # First remove code blocks
        content = self._remove_code_blocks(self._content)
        
        # Match [[link]] or [[link|alias]] patterns
        link_pattern = r'\[\[(.*?)(?:\|(.*?))?\]\]'
        matches = re.finditer(link_pattern, content)
        
        for match in matches:
            target = match.group(1).strip()
            alias = match.group(2).strip() if match.group(2) else None
            
            # Strip formatting characters from target and alias
            target = re.sub(r'[*_"`]', '', target)
            if alias:
                alias = re.sub(r'[*_"`]', '', alias)
            
            # Skip links in code blocks
            if '```' in target or '`' in target:
                continue
            
            links.append(Link(target=target, alias=alias))
        
        return links

    @property
    def path(self) -> str:
        """Get the path of the note."""
        return self._path

    @property
    def content(self) -> str:
        """Get the content of the note."""
        return self._content

    @property
    def title(self) -> str:
        """Get the title of the note."""
        return self._title

    @property
    def links(self) -> List[Link]:
        """Get the links in the note."""
        return self._links

    @property
    def filename(self) -> str:
        """Get the filename of the note."""
        return os.path.basename(self._path)

    def update_content(self, content: str) -> None:
        """Update the note content and recalculate metadata.

        Args:
            content: The new content for the note.
        """
        self._content = content
        self._title = self._extract_title()
        self._links = self._extract_links()

    def add_tag(self, tag: str) -> None:
        """Add a tag to the note.
        
        Args:
            tag: The tag to add (without the # prefix).
        """
        # Strip # from tag if present
        tag = tag.lstrip('#')
        
        # Check if tag already exists
        if tag in self.tags:
            return
        
        # Add tag at the end of the first line that's not a header
        lines = self._content.splitlines()
        header_end = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith('#'):
                header_end = i
                break
        
        # Add the tag
        if header_end < len(lines):
            lines[header_end] = f"{lines[header_end]} #{tag}"
        else:
            lines.append(f"#{tag}")
        
        # Update content
        self.update_content('\n'.join(lines))

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the note.
        
        Args:
            tag: The tag to remove (without the # prefix).
        """
        # Strip # from tag if present
        tag = tag.lstrip('#')
        
        # Check if tag exists
        if tag not in self.tags:
            return
        
        # Remove the tag using regex
        content = self._content
        content = re.sub(f'#({tag})(?![\\w-])', '', content)
        
        # Clean up any resulting double spaces
        content = re.sub(r' +', ' ', content)
        
        # Update content
        self.update_content(content)

    def __repr__(self) -> str:
        """Get a string representation of the note."""
        return f"Note(path={self.path}, title={self.title})"


class Vault:
    """A vault containing notes."""

    def __init__(self, vault_path: Union[str, Path]) -> None:
        """Initialize a vault.

        Args:
            vault_path: Path to the vault directory.
        """
        self.vault_path = Path(vault_path)
        self.notes: Dict[str, Note] = {}
        self._load_notes()

    def _get_all_files(self) -> List[str]:
        """Get all markdown files in the vault."""
        if not self.vault_path.exists():
            return []

        markdown_files = []
        for file_path in self.vault_path.rglob("*.md"):
            try:
                rel_path = file_path.relative_to(self.vault_path)
                markdown_files.append(str(rel_path))
            except ValueError:
                continue
        return markdown_files

    def _load_notes(self) -> None:
        """Load all notes from the vault."""
        self.notes.clear()
        for file_path in self._get_all_files():
            try:
                note_path = self.vault_path / file_path
                if note_path.exists():
                    content = note_path.read_text()
                    self.notes[file_path] = Note(file_path, content)
            except (OSError, UnicodeDecodeError):
                continue

    def get_note(self, path: str) -> Optional[Note]:
        """Get a note by its path."""
        return self.notes.get(path)

    def note_exists(self, target: str) -> bool:
        """Check if a note exists in the vault.
        
        Args:
            target: The target path or name of the note.
            
        Returns:
            bool: True if the note exists, False otherwise.
        """
        # Try with and without .md extension
        target_with_md = f"{target}.md" if not target.endswith('.md') else target
        target_without_md = target[:-3] if target.endswith('.md') else target
        
        # Check if either version exists in notes
        return any(
            note.path.endswith(target_with_md) or 
            note.path.endswith(target_without_md) 
            for note in self.notes.values()
        )

    def get_all_notes(self) -> List[Note]:
        """Get all notes in the vault."""
        return list(self.notes.values())

    def create_note(self, title: str, content: str = "") -> Note:
        """Create a new note in the vault.

        Args:
            title: The title of the note.
            content: Optional initial content for the note.

        Returns:
            The created note.
        """
        filename = f"{title.lower().replace(' ', '_')}.md"
        path = str(self.vault_path / filename)
        if not content:
            content = f"# {title}\n"
        with open(path, "w") as f:
            f.write(content)
        note = Note(filename, content)
        self.notes[filename] = note
        return note

    def update_note(self, path: str, content: str) -> None:
        """Update a note's content.

        Args:
            path: The path to the note.
            content: The new content for the note.
        """
        note_path = self.vault_path / path
        with open(note_path, "w") as f:
            f.write(content)
        if path in self.notes:
            self.notes[path].update_content(content)

    def delete_note(self, path: str) -> None:
        """Delete a note from the vault.

        Args:
            path: The path to the note.
        """
        note_path = self.vault_path / path
        if note_path.exists():
            note_path.unlink()
        if path in self.notes:
            del self.notes[path]

    def get_empty_folders(self) -> List[str]:
        """Get all empty folders in the vault."""
        empty_folders = []
        for folder in self.vault_path.rglob("*"):
            if folder.is_dir():
                try:
                    rel_path = str(folder.relative_to(self.vault_path))
                    if not list(folder.iterdir()):
                        empty_folders.append(rel_path)
                except ValueError:
                    continue
        return empty_folders

    def get_empty_notes(self) -> List[Note]:
        """Get all notes with zero word count."""
        return [note for note in self.notes.values() if note.word_count == 0]

    def get_small_notes(self, min_words: int = 50) -> List[Note]:
        """Get notes with fewer than min_words words."""
        return [note for note in self.notes.values() if 0 < note.word_count < min_words]

    def get_broken_links(self) -> List[Note]:
        """Get notes with broken links."""
        broken_notes = []
        note_paths = {note.path for note in self.notes.values()}
        for note in self.notes.values():
            for link in note.links:
                target_path = f"{link.target}.md"
                if target_path not in note_paths:
                    broken_notes.append(note)
                    break
        return broken_notes

    def get_orphan_notes(self, include_empty: bool = False) -> List[Note]:
        """Get orphaned notes (not linked from anywhere)."""
        linked_paths = set()
        for note in self.notes.values():
            for link in note.links:
                linked_paths.add(f"{link.target}.md")

        orphan_notes = []
        for note in self.notes.values():
            if note.path not in linked_paths:
                if include_empty:
                    orphan_notes.append(note)
                elif note.word_count > 0:
                    orphan_notes.append(note)
        return orphan_notes

    def get_all_tags(self) -> Dict[str, int]:
        """Get all tags and their usage count."""
        tag_counts: Dict[str, int] = {}
        for note in self.notes.values():
            for tag in note.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return tag_counts

    def get_notes_by_tag(self, tag: str) -> List[Note]:
        """Get all notes with a specific tag."""
        tag = tag.lstrip('#')
        return [note for note in self.notes.values() if tag in note.tags]

    def search_notes(self, query: str, case_sensitive: bool = False) -> List[Note]:
        """Search for notes containing a query string."""
        if not case_sensitive:
            query = query.lower()
        matching_notes = []
        for note in self.notes.values():
            content = note.content if case_sensitive else note.content.lower()
            title = note.title if case_sensitive else note.title.lower()
            if query in content or query in title:
                matching_notes.append(note)
        return matching_notes


class ObsidianContext:
    """A singleton context for the Obsidian vault."""

    _instance = None

    def __new__(cls) -> "ObsidianContext":
        """Create a new ObsidianContext instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.vault = None
        return cls._instance

    def __init__(self) -> None:
        """Initialize the context."""
        if self.vault is None:
            self.vault = Vault(Path.cwd())

    def set_vault_path(self, vault_path: Union[str, Path]) -> None:
        """Set the vault path and initialize the vault.

        Args:
            vault_path: The path to the vault directory.
        """
        self.vault = Vault(vault_path)

    def run(self, command_handler: Callable[[str, "ObsidianContext"], None]) -> None:
        """Run the Obsidian CLI application."""
        while True:
            command = input(
                "Enter command (list, view, create, update, delete, exit): "
            )
            if command == "exit":
                break
            command_handler(command, self)


obsidian_context = ObsidianContext()
