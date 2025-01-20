import re
from typing import List, Optional, Set
from pyobsidian.link import Link

class Note:
    """A class representing a note in an Obsidian vault."""

    def __init__(self, path: str, content: str = "") -> None:
        """Initialize a note."""
        self._path = path
        self._content = content
        self._title = self._extract_title()
        self._tags = self._extract_tags()
        self._links = self._extract_links()

    @property
    def content(self) -> str:
        """Get the content of the note."""
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        """Set the content of the note."""
        self._content = value
        self._title = self._extract_title()
        self._tags = self._extract_tags()
        self._links = self._extract_links()

    @property
    def title(self) -> str:
        """Get the note's title."""
        return self._title

    @property
    def tags(self) -> List[str]:
        """Get the note's tags."""
        return self._tags

    @property
    def links(self) -> List[Link]:
        """Get the note's links."""
        return self._links

    @property
    def word_count(self) -> int:
        """Calculate the number of words in the note content."""
        # Remove code blocks first
        content = self._remove_code_blocks(self._content)
        
        # Remove YAML frontmatter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        
        # Remove links and tags
        content = re.sub(r'\[\[.*?\]\]', '', content)
        content = re.sub(r'#\w+', '', content)
        
        # Remove headers (but keep the title text)
        title_words = []
        if self.title:
            title_words = [w for w in self.title.split() if w.strip() and not w.isdigit()]
        content = re.sub(r'^#+\s.*$', '', content, flags=re.MULTILINE)
        
        # Remove formatting characters and punctuation
        content = re.sub(r'[*_`]', '', content)
        content = re.sub(r'[^\w\s]', ' ', content)
        
        # Normalize whitespace
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        # Count non-empty words
        content_words = [word for word in content.split() if word.strip() and not word.isdigit()]
        return len(title_words) + len(content_words)

    @property
    def path(self) -> str:
        """Get the note's path."""
        return self._path

    def _extract_title(self) -> str:
        """Extract the title from the note's content."""
        if not self._content:
            return ""
        lines = self._content.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("# "):
                # Remove emphasis markers from title
                title = line[2:].strip()
                title = re.sub(r'(\*\*|\*|__|_)', '', title)
                return title
        return ""

    def _extract_tags(self) -> List[str]:
        """Extract tags from the note's content."""
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
            # Skip tags with emphasis markers
            if any(marker in tag for marker in ['*', '_', '`']):
                continue
            if tag not in seen:
                seen.add(tag)
                tags.append(tag)
        
        return sorted(tags)

    def _extract_links(self) -> List[Link]:
        """Extract all links from the note content."""
        links = []
        content = self._remove_code_blocks(self._content)
        link_pattern = r'\[\[(.*?)(?:\|(.*?))?\]\]'
        matches = re.finditer(link_pattern, content)
        
        for match in matches:
            target = match.group(1).strip()
            alias = match.group(2).strip() if match.group(2) else None
            
            # Remove formatting characters and quotes
            target = re.sub(r'(\*\*|\*|__|_|`|```)', '', target).strip()
            target = target.strip('"')
            if alias:
                alias = re.sub(r'(\*\*|\*|__|_|`|```)', '', alias).strip()
                alias = alias.strip('"')
            
            # Skip empty targets
            if not target:
                continue
            
            links.append(Link(target=target, alias=alias))
        return links

    def _remove_code_blocks(self, content: str) -> str:
        """Remove code blocks from content."""
        # Remove fenced code blocks
        content = re.sub(r'```[^`]*```', '', content, flags=re.DOTALL)
        # Remove inline code
        content = re.sub(r'`[^`]+`', '', content)
        return content

    def update_content(self, content: str) -> None:
        """Update the note's content."""
        self._content = content
        self._title = self._extract_title()
        self._tags = self._extract_tags()
        self._links = self._extract_links()

    def add_tag(self, tag: str) -> None:
        """Add a tag to the note."""
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
        self._content = '\n'.join(lines)
        if not self._content.endswith('\n'):
            self._content += '\n'
        self._tags = self._extract_tags()

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the note."""
        # Strip # from tag if present
        tag = tag.lstrip('#')
        
        # Check if tag exists
        if tag not in self.tags:
            return
        
        # Remove tag using regex
        self._content = re.sub(rf'\s*#({re.escape(tag)})(?![\\w-])', '', self._content)
        self._content = re.sub(r'\s+', ' ', self._content).strip()
        if not self._content.endswith('\n'):
            self._content += '\n'
        
        # Update tags
        self._tags = self._extract_tags()

    def save(self) -> None:
        """Save the note's content to disk."""
        obsidian_context.vault.update_note(self.path, self._content)

    def __lt__(self, other: "Note") -> bool:
        """Compare notes by path for sorting."""
        return self.path < other.path

    def __repr__(self) -> str:
        """Get a string representation of the note."""
        return f"Note(path='{self.path}', title='{self._title}')" 