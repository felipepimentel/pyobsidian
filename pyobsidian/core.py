from __future__ import annotations

import os
import re
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Pattern

import yaml


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
    def __init__(self, source: "Note", target: str, alias: Optional[str] = None):
        self.source: "Note" = source
        self.target: str = target
        self.alias: Optional[str] = alias


class Note:
    def __init__(self, path: str, content: str):
        self.path: str = path
        self.content: str = content
        self.name: str = os.path.splitext(os.path.basename(path))[0]  # Novo atributo
        self.title: str = self._extract_title()
        self.tags: List[str] = self._extract_tags()
        self.links: List[Link] = self._extract_links()
        self.created_at: Optional[datetime] = None
        self.updated_at: Optional[datetime] = None

    def _extract_title(self) -> str:
        first_line = self.content.split("\n", 1)[0].strip()
        return first_line.lstrip("#").strip() if first_line.startswith("#") else ""

    def _extract_tags(self) -> List[str]:
        return re.findall(r"#(\w+)", self.content)

    def _extract_links(self) -> List[Link]:
        links = []
        for match in re.finditer(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", self.content):
            target = match.group(1)
            alias = match.group(2)
            links.append(Link(self, target, alias))
        return links

    @property
    def filename(self) -> str:
        return os.path.basename(self.path)

    @property
    def file_size(self) -> int:
        return len(self.content)

    def update_content(self, new_content: str) -> None:
        self.content = new_content
        self.updated_at = datetime.now()
        self.tags = self._extract_tags()
        self.links = self._extract_links()

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def __str__(self) -> str:
        return self.path

    def __repr__(self) -> str:
        return f"Note(path={self.path}, title={self.title})"

    @property
    def word_count(self) -> int:
        """Calculate the word count of the note."""
        return len(self.content.split())


class Vault:
    def __init__(self, config: Config):
        self.config = config
        self.notes: Dict[str, Note] = self._load_notes()

    def _load_notes(self) -> Dict[str, Note]:
        notes = {}
        for file_path in self._get_all_files():
            content = self._get_file_content(file_path)
            notes[file_path] = Note(file_path, content)
        return notes

    def _get_all_files(self) -> List[str]:
        if not self.config.vault_path:
            raise FileOperationError("Vault path is not set in the configuration.")
        try:
            all_files = []
            for root, dirs, files in os.walk(self.config.vault_path):
                dirs[:] = [
                    d for d in dirs if not self._is_excluded(os.path.join(root, d))
                ]
                for file in files:
                    if file.endswith(".md"):
                        file_path = os.path.join(root, file)
                        if not self._is_excluded(file_path):
                            all_files.append(file_path)
            return all_files
        except Exception as e:
            raise FileOperationError(f"Error listing files in vault: {str(e)}")

    def _is_excluded(self, path: str) -> bool:
        relative_path = os.path.relpath(path, self.config.vault_path)
        return any(
            pattern.search(relative_path) for pattern in self.config.excluded_patterns
        )

    def _get_file_content(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise FileOperationError(f"Error reading file {file_path}: {str(e)}")

    def get_note(self, path: str) -> Optional[Note]:
        return self.notes.get(path)

    def get_all_notes(self) -> List[Note]:
        return list(self.notes.values())

    def create_note(self, title: str, content: str) -> Note:
        filename = f"{title.lower().replace(' ', '_')}.md"
        path = os.path.join(self.config.vault_path, filename)

        if os.path.exists(path):
            raise FileOperationError(f"Note already exists: {path}")

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\n{content}")

            note = Note(path, f"# {title}\n\n{content}")
            self.notes[path] = note
            return note
        except Exception as e:
            raise FileOperationError(f"Error creating note: {str(e)}")

    def update_note(self, path: str, new_content: str) -> Note:
        note = self.get_note(path)
        if not note:
            raise FileOperationError(f"Note not found: {path}")

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            note.update_content(new_content)
            return note
        except Exception as e:
            raise FileOperationError(f"Error updating note: {str(e)}")

    def delete_note(self, note: Note) -> None:
        """
        Delete a single note from the vault.

        Args:
            note (Note): The note to be deleted.

        Raises:
            FileOperationError: If there's an error during deletion.
        """
        try:
            os.remove(note.path)
            del self.notes[note.path]
        except Exception as e:
            raise FileOperationError(f"Error deleting note: {str(e)}")

    def delete_notes(self, notes: List[Note]) -> None:
        """
        Delete multiple notes from the vault.

        Args:
            notes (List[Note]): A list of notes to be deleted.

        Raises:
            FileOperationError: If there's an error during deletion of any note.
        """
        for note in notes:
            self.delete_note(note)


class ObsidianContext:
    _instance = None

    def __new__(cls, config_path: str = "config.yaml"):
        if cls._instance is None:
            cls._instance = super(ObsidianContext, cls).__new__(cls)
            cls._instance.config = Config(config_path)
            cls._instance.vault = Vault(cls._instance.config)
        return cls._instance

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
