"""Tests for markdown parsing and handling functionality."""
from typing import TYPE_CHECKING
import pytest
from pyobsidian.core import Note

def test_markdown_headers():
    """Test parsing of different header levels and formats."""
    content = """# H1 Header
    ## H2 Header
    ### H3 Header
    #### H4 Header
    ##### H5 Header
    ###### H6 Header
    
    Alternative H1
    =============
    
    Alternative H2
    -------------
    """
    note = Note("test.md", content)
    assert note.title == "H1 Header"  # Should get first H1

def test_markdown_lists():
    """Test handling of markdown lists with embedded elements."""
    content = """# Lists Test
    
    - Unordered list item with #tag
    - Item with [[link]]
    - Item with [[link|alias]]
    
    1. Ordered list with #tag
    2. Item with [[link]]
    3. Item with [[link|alias]]
    
    * Alternative unordered
    * With #multiple #tags
    * And [[multiple]] [[links]]
    """
    note = Note("test.md", content)
    
    # Check tags are found in lists
    assert "tag" in note.tags
    assert "multiple" in note.tags
    
    # Check links are found in lists
    link_targets = {link.target for link in note.links}
    assert "link" in link_targets
    assert "multiple" in link_targets

def test_markdown_code_blocks():
    """Test handling of code blocks and inline code."""
    content = """# Code Blocks
    
    Here's `inline code` with a #tag.
    
    ```python
    def function():
        # This #tag should not be counted
        print("[[this link]] should not be counted")
    ```
    
    ```
    Generic code block
    #tag should not be counted
    [[link]] should not be counted
    ```
    
    ``#tag in double backticks``
    """
    note = Note("test.md", content)
    
    # Only the tag outside code blocks should be counted
    assert len(note.tags) == 1
    assert "tag" in note.tags
    
    # No links should be found (they're all in code blocks)
    assert len(note.links) == 0

def test_markdown_emphasis():
    """Test handling of emphasis and strong emphasis with embedded elements."""
    content = """# Emphasis Test
    
    *Italic text with #tag*
    **Bold text with #another-tag**
    ***Bold italic with #third-tag***
    
    _Alternative italic with [[link]]_
    __Alternative bold with [[another-link]]__
    ___Alternative bold italic with [[third-link]]___
    
    *Mixed **formats** with #tags and [[links]]*
    """
    note = Note("test.md", content)
    
    # Check all tags are found
    assert "tag" in note.tags
    assert "another-tag" in note.tags
    assert "third-tag" in note.tags
    
    # Check all links are found
    link_targets = {link.target for link in note.links}
    assert "link" in link_targets
    assert "another-link" in link_targets
    assert "third-link" in link_targets

def test_markdown_blockquotes():
    """Test handling of blockquotes with embedded elements."""
    content = """# Blockquotes Test
    
    > Simple blockquote with #tag
    > And a [[link]]
    
    > Multiline blockquote
    > with #multiple #tags
    > and [[multiple]] [[links]]
    
    > Nested blockquotes
    >> with #nested #tags
    >> and [[nested]] [[links]]
    """
    note = Note("test.md", content)
    
    # Check tags in blockquotes
    assert "tag" in note.tags
    assert "multiple" in note.tags
    assert "nested" in note.tags
    
    # Check links in blockquotes
    link_targets = {link.target for link in note.links}
    assert "link" in link_targets
    assert "multiple" in link_targets
    assert "nested" in link_targets

def test_markdown_tables() -> None:
    """Test that links are correctly extracted from markdown tables."""
    content = """
| Column 1 | Column 2 |
|----------|----------|
| [[link1]] | [[link2]] |
| [[link3]] | [[link4]] |
"""
    note = Note("test.md", content)
    link_targets = {link.target for link in note._extract_links()}
    expected_links = {"link1", "link2", "link3", "link4"}
    assert link_targets == expected_links 