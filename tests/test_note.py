"""Tests for Note class functionality."""
from typing import TYPE_CHECKING
import pytest
from pyobsidian.core import Note, Link

@pytest.fixture
def simple_note_content() -> str:
    """Fixture providing content for a simple note."""
    return """# Simple Note
    This is a simple note with basic content.
    It has a #tag and a [[link]].
    """

@pytest.fixture
def complex_note_content() -> str:
    """Fixture providing content for a complex note with various markdown elements."""
    return """# Complex Note
    Here's a paragraph with a [[simple link]] embedded.
    
    And here's one with a [[complex/path/to/note|custom name]].
    
    - List item with [[link]]
    - Another with [[spaced link name]]
    
    > Blockquote with [[quoted link|alias]]
    
    ```markdown
    Code block with [[code link]] that should be ignored
    ```
    
    *Italic text with [[italic link]]* and **bold with [[bold link]]**
    """

@pytest.fixture
def tag_note_content() -> str:
    """Fixture providing content for testing tag extraction."""
    return """# Note with Tags
    This is a note with #python and #testing tags.
    Also has a #compound-tag and #123numeric tags.
    But not a # broken tag or #!invalid one.
    
    ```python
    # This is a code comment, not a tag
    def func():
        pass  # Also not a #tag
    ```
    """

@pytest.fixture
def word_count_note_content() -> str:
    """Fixture providing content for testing word count calculation."""
    return """# Title with three words
    This paragraph has five words.
    
    And this one has four.
    
    #tags don't count as #words
    [[links]] don't count either
    
    ```python
    # Code blocks should be ignored
    def func():
        pass
    ```
    """

def test_note_title_extraction():
    """Test that titles are correctly extracted from markdown content."""
    # Test with H1 header
    content = "# My Test Note\nThis is content"
    note = Note("test.md", content)
    assert note.title == "My Test Note"
    
    # Test without header
    content = "This is content without header"
    note = Note("test.md", content)
    assert note.title == ""
    
    # Test with multiple headers
    content = "# Main Title\n## Subtitle\nContent"
    note = Note("test.md", content)
    assert note.title == "Main Title"

def test_note_tags_extraction(tag_note_content):
    """Test that tags are correctly extracted from markdown content."""
    note = Note("test.md", tag_note_content)
    assert set(note.tags) == {"python", "testing", "compound-tag", "123numeric"}

def test_note_links_extraction() -> None:
    """Test that links are correctly extracted from note content."""
    content = """
# Test Note

[[simple link]]
[[spaced link name]]
[[complex/path/to/note]]
[[*italic link*]]
[[**bold link**]]
[["quoted link"]]
"""
    note = Note("test.md", content)
    link_targets = {link.target for link in note._extract_links()}
    expected_targets = {
        "simple link",
        "spaced link name",
        "complex/path/to/note",
        "italic link",
        "bold link",
        "quoted link"
    }
    assert link_targets == expected_targets

def test_note_content_update() -> None:
    """Test that note content can be updated."""
    note = Note("test.md", "# Original Title\nThis is a [[link]] to another note.")
    new_content = "# New Title\nThis is a [[new link]] to a different note."
    note.update_content(new_content)
    assert note.title == "New Title"
    assert note.links[0].target == "new link"

def test_note_add_tag(simple_note_content):
    """Test that tags can be added to a note."""
    note = Note("test.md", simple_note_content)
    
    assert "tag" in note.tags
    assert len(note.tags) == 1
    
    note.add_tag("new")
    assert "new" in note.tags
    assert len(note.tags) == 2
    
    # Adding same tag again shouldn't duplicate
    note.add_tag("new")
    assert len(note.tags) == 2 