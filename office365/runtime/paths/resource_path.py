from __future__ import annotations

from typing import Iterator, Optional, Union

from typing_extensions import Self


class ResourcePath:
    """
    Represents an OData resource path used for constructing API endpoint URLs.

    This class handles path segment construction and provides methods for navigating
    and manipulating resource paths in a hierarchical manner.
    """

    def __init__(
        self,
        segment: Optional[Union[int, str]] = None,
        parent: Optional["ResourcePath"] = None,
    ) -> None:
        """
        Initialize a new resource path segment.

        Args:
            segment: The identifier for this path segment (e.g., item ID or name)
            parent: The parent path segment (None for root segments)
        """
        self._key = segment
        self._parent = parent

    def set_key(self, segment: Union[int, str]) -> Self:
        """
        Updates the path segment key if not already set.

        Args:
            key: The identifier to set for this path segment

        Returns:
            self: Supports method chaining

        Example:
            >>> path = ResourcePath().set_key("items")
        """
        if self._key is None:
            self._key = segment
        return self

    def __iter__(self) -> Iterator[ResourcePath]:
        """
        Iterates through the path hierarchy from leaf to root.

        Yields:
            ResourcePath: Each path segment in the hierarchy

        Example:
            >>> res_path = ResourcePath("items", ResourcePath("lists"))
            >>> for segment in res_path:
            ...     print(segment.segment)
        """
        current = self
        while current:
            yield current
            current = current.parent

    def __repr__(self):
        """Official string representation of the full path."""
        return self.to_url()

    def __str__(self):
        """String representation of the full path (same as to_url())."""
        return self.to_url()

    def __eq__(self, other: object) -> bool:
        """
        Compares two resource paths for equality based on their URL representation.

        Args:
            other: Another object to compare with

        Returns:
            bool: True if paths are equivalent
        """
        if not isinstance(other, ResourcePath):
            return NotImplemented
        return self.to_url() == other.to_url()

    __hash__ = None  # type: ignore[assignment]

    def to_url(self) -> str:
        """
        Constructs the full URL path by combining all segments.

        Returns:
            str: The complete path string

        Example:
            >>> res_path = ResourcePath("items", ResourcePath("lists"))
            >>> res_path.to_url()  # Returns "/lists/items"
        """
        segments = []
        for path in self:
            segments.insert(0, path.segment)
            if path.delimiter:
                segments.insert(0, path.delimiter)
        return "".join(segments)

    @property
    def parent(self) -> Optional[ResourcePath]:
        """Gets the parent path segment."""
        return self._parent

    @property
    def segment(self) -> str:
        """Gets the current path segment as a string."""
        return str(self._key)

    @property
    def delimiter(self) -> str | None:
        """Gets the path delimiter (always '/' for OData)."""
        return "/"
