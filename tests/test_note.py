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

def test_note_links_extraction(complex_note_content):
    """Test that internal links are correctly extracted from markdown content."""
    note = Note("test.md", complex_note_content)
    
    # Verify all links were found (excluding those in code blocks)
    link_targets = {link.target for link in note.links}
    expected_targets = {
        "simple link",
        "complex/path/to/note",
        "link",
        "spaced link name",
        "quoted link",
        "italic link",
        "bold link"
    }
    assert link_targets == expected_targets
    
    # Check specific link properties
    aliased_link = next(link for link in note.links if link.target == "complex/path/to/note")
    assert aliased_link.alias == "custom name"
    
    quoted_link = next(link for link in note.links if link.target == "quoted link")
    assert quoted_link.alias == "alias"

def test_note_content_update(simple_note_content):
    """Test that note content can be updated and metadata is recalculated."""
    note = Note("test.md", simple_note_content)
    assert "tag" in note.tags
    assert len(note.links) == 1
    assert note.links[0].target == "link"
    
    # Update content
    new_content = "# Updated Note\nWith #new tag and [[new link|alias]]"
    note.update_content(new_content)
    
    assert note.title == "Updated Note"
    assert "new" in note.tags
    assert "tag" not in note.tags
    assert len(note.links) == 1
    assert note.links[0].target == "new link"
    assert note.links[0].alias == "alias"

def test_note_word_count(word_count_note_content):
    """Test that word count is calculated correctly."""
    note = Note("test.md", word_count_note_content)
    # Should count: Title(3) + This(1) + paragraph(1) + has(1) + five(1) + words(1) +
    # And(1) + this(1) + one(1) + has(1) + four(1) = 12 words
    assert note.word_count == 12

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