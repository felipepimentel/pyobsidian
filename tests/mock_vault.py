class MockVault:
    """Mock vault for testing."""
    
    def __init__(self) -> None:
        """Initialize the mock vault."""
        self._notes = {}
        self._setup_test_notes()
    
    def _setup_test_notes(self) -> None:
        """Set up test notes with known content."""
        # note1.md: A test note with many words
        self._notes["note1.md"] = Note("note1.md", """# Test Note
This is a test note with many words. It contains links to [[note2]] and [[note3]].
It also has some #tags and #more_tags to test with.
This note is long enough to not be considered small.
Additional content to ensure it has more than 5 words.""")
        
        # note2.md: An empty note
        self._notes["note2.md"] = Note("note2.md", "")
        
        # note3.md: A note about Python development
        self._notes["note3.md"] = Note("note3.md", """# Python Development
This note covers Python programming concepts.
It links back to [[note1]] and contains #python and #development tags.
More content to ensure it has more than 5 words.""")
        
        # note4.md: A short note with exactly 4 words
        self._notes["note4.md"] = Note("note4.md", """Brief text only #short""")
        
        # note5.md: A note with exactly 3 words
        self._notes["note5.md"] = Note("note5.md", """Just three words""")
        
        # note6.md: A note with exactly 2 words
        self._notes["note6.md"] = Note("note6.md", """Two words""")
        
        # folder1/nested_note.md: A note with exactly 5 words
        self._notes["folder1/nested_note.md"] = Note("folder1/nested_note.md", """Five words in this note""")
        
        # folder2/another_note.md: A note with more than 5 words
        self._notes["folder2/another_note.md"] = Note("folder2/another_note.md", """This note has more than five words""")
        
        # complex_note.md: A note with complex formatting
        self._notes["complex_note.md"] = Note("complex_note.md", """# Complex Note
Links with formatting: [[*italic link*]], [[**bold link**]], [[`code link`]], [["quoted link"]].
A table with links:
| Column 1 | Column 2 |
|----------|----------|
| [[link1]] | [[link2]] |
| [[link3]] | [[link4]] |""")
        
        # python_note.md: A note about Python
        self._notes["python_note.md"] = Note("python_note.md", """# Python Programming
Python is a versatile programming language.
#python #programming""")
        
        # programming_note.md: A note about programming
        self._notes["programming_note.md"] = Note("programming_note.md", """# Programming Basics
Basic programming concepts and principles.
#programming #basics""")
        
        # unrelated_note.md: A note about cooking
        self._notes["unrelated_note.md"] = Note("unrelated_note.md", """# Cooking Tips
Some cooking tips and recipes.
#cooking #tips""")
        
        # source.md: A source note for similarity testing
        self._notes["source.md"] = Note("source.md", """# Source Note
This is a source note for testing similarity.
It contains some common words and phrases.""")
        
        # empty.md: An empty note for similarity testing
        self._notes["empty.md"] = Note("empty.md", "")
    
    def exists(self, path: str) -> bool:
        """Check if a path exists in the vault."""
        return path in self._notes or path in ["empty_folder"]
    
    def is_file(self, path: str) -> bool:
        """Check if a path is a file."""
        return path in self._notes
    
    def is_dir(self, path: str) -> bool:
        """Check if a path is a directory."""
        return path == "empty_folder" or any(note_path.startswith(f"{path}/") for note_path in self._notes)
    
    def get_all_files(self) -> List[str]:
        """Get all file paths in the vault."""
        return list(self._notes.keys())
    
    def get_folders(self) -> List[str]:
        """Get all folder paths in the vault."""
        folders = {"empty_folder"}
        for path in self._notes:
            if "/" in path:
                folders.add(path.split("/")[0])
        return sorted(folders)
    
    def read_file(self, path: str) -> str:
        """Read a file's content."""
        if path not in self._notes:
            raise ValueError(f"File {path} not found")
        return self._notes[path].content
    
    def write_file(self, path: str, content: str) -> None:
        """Write content to a file."""
        self._notes[path] = Note(path, content)
    
    def get_note(self, path: str) -> Note:
        """Get a note by its path."""
        if path not in self._notes:
            raise ValueError(f"Note {path} not found")
        return self._notes[path]
    
    def get_all_notes(self) -> List[Note]:
        """Get all notes in the vault."""
        return list(self._notes.values())
    
    def get_all_tags(self) -> Dict[str, int]:
        """Get all tags and their counts."""
        tag_counts = {}
        for note in self._notes.values():
            for tag in note.tags:
                tag = tag.lstrip('#')
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return tag_counts
    
    def get_notes_by_tag(self, tag: str) -> List[Note]:
        """Get all notes with a specific tag."""
        tag = f"#{tag.lstrip('#')}"
        return [note for note in self._notes.values() if tag in note.content]
    
    def update_note(self, path: str, content: str) -> None:
        """Update a note's content."""
        if path not in self._notes:
            raise ValueError(f"Note {path} not found")
        self._notes[path].update_content(content)
    
    def get_empty_notes(self) -> List[Note]:
        """Get all empty notes."""
        return [note for note in self._notes.values() if not note.content.strip()]
    
    def get_small_notes(self, max_words: int) -> List[Note]:
        """Get all notes with few words."""
        return [note for note in self._notes.values() if note.word_count <= max_words]
    
    def get_broken_links(self) -> Dict[str, List[str]]:
        """Get all broken links in notes."""
        broken_links = {}
        for note in self._notes.values():
            invalid_links = []
            for link in note.links:
                target = link.target
                if not target.endswith('.md'):
                    target += '.md'
                if target not in self._notes:
                    invalid_links.append(link.target)
            if invalid_links:
                broken_links[note.path] = invalid_links
        return broken_links
    
    def get_orphan_notes(self) -> List[Note]:
        """Get all notes that are not linked to by any other note."""
        linked_notes = set()
        for note in self._notes.values():
            for link in note.links:
                target = link.target
                if not target.endswith('.md'):
                    target += '.md'
                linked_notes.add(target)
        return [note for note in self._notes.values() if note.path not in linked_notes]
    
    def get_statistics(self) -> Dict[str, int]:
        """Get vault statistics."""
        return {
            "total_notes": len(self._notes),
            "total_tags": len(self.get_all_tags()),
            "empty_notes": len(self.get_empty_notes()),
            "orphan_notes": len(self.get_orphan_notes()),
            "broken_links": sum(len(links) for links in self.get_broken_links().values())
        } 