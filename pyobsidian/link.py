"""Link class for PyObsidian."""
from typing import Optional, Union

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

    def __lt__(self, other: "Link") -> bool:
        """Compare links for sorting."""
        return (self.source, self.target) < (other.source, other.target) 