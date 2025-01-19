import re
from typing import List
from .link import Link

class Note:
    @property
    def word_count(self) -> int:
        """Get the number of words in the note content."""
        # Remove code blocks
        content = self.content
        cleaned_lines = []
        in_code_block = False
        for line in content.split('\n'):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if not in_code_block:
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Remove inline code
        content = re.sub(r'`[^`]+`', '', content)
        
        # Remove tags
        content = re.sub(r'#[\w-]+', '', content)
        
        # Remove links
        content = re.sub(r'\[\[.*?\]\]', '', content)
        
        # Remove headers
        content = re.sub(r'^#\s.*$', '', content, flags=re.MULTILINE)
        
        # Remove punctuation and normalize whitespace
        content = re.sub(r'[^\w\s-]', ' ', content)
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Split into words and count only those with letters
        words = [word for word in content.split() if any(c.isalpha() for c in word)]
        
        # Remove duplicates
        words = list(dict.fromkeys(words))
        
        return len(words)

    @property
    def links(self) -> List[Link]:
        """Get all links in the note content."""
        links = []
        # Split content into lines
        lines = self.content.split('\n')
        in_code_block = False
        
        # Process each line
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if not in_code_block:
                # Match [[target]] or [[target|alias]]
                pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
                matches = re.finditer(pattern, line)
                for match in matches:
                    target = match.group(1).strip()
                    alias = match.group(2).strip() if match.group(2) else None
                    links.append(Link(self.path, target, alias))
        
        return links 