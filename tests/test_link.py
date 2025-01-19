"""Tests for Link class functionality."""
from typing import TYPE_CHECKING
import pytest
from pyobsidian.core import Note, Link

def test_link_creation():
    """Test that links are created correctly with and without aliases."""
    source_note = Note("source.md", "# Source Note")
    
    # Simple link
    simple_link = Link(source_note, "target")
    assert simple_link.source == source_note
    assert simple_link.target == "target"
    assert simple_link.alias is None
    
    # Link with alias
    aliased_link = Link(source_note, "target", "display name")
    assert aliased_link.source == source_note
    assert aliased_link.target == "target"
    assert aliased_link.alias == "display name"

def test_link_in_complex_note() -> None:
    """Test link extraction from a complex note with various markdown elements."""
    content = """# Title
This is a **[[bold link]]** and *[[italic link]]*.
Here's a `[[code link]]` and a [[[markdown link]]].
```python
[[code block link]]
```
> [[quoted link]]
"""
    note = Note(path="test.md", content=content)
    link_targets = {link.target for link in note.links}
    expected_targets = {
        "bold link",
        "italic link",
        "markdown link",
        "quoted link"
    }
    assert link_targets == expected_targets 