from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional, Tuple


@dataclass
class QueryOptions:
    """Represents OData query options for controlling data requests.

    Encapsulates all standard OData system query options ($select, $filter, etc.)
    and supports custom query parameters.

    Attributes:
        select: List of properties to include ($select)
        expand: List of related resources to expand ($expand)
        filter: Filter expression ($filter)
        order_by: Sorting criteria ($orderby)
        top: Maximum items to return ($top)
        skip: Number of items to skip ($skip)
        custom: Dictionary of custom query parameters
    """

    select: List[str] = field(default_factory=list)
    expand: List[str] = field(default_factory=list)
    filter: Optional[str] = None
    order_by: Optional[str] = None
    top: Optional[int] = None
    skip: Optional[int] = None
    custom: Dict[str, str] = field(default_factory=dict)

    def reset(self) -> None:
        """Resets all query options to default/empty values."""
        self.select.clear()
        self.expand.clear()
        self.filter = None
        self.order_by = None
        self.skip = None
        self.top = None
        self.custom.clear()

    def __repr__(self):
        return self.to_url()

    def __str__(self):
        return self.to_url()

    @property
    def is_empty(self) -> bool:
        """Checks if any query options are set."""
        return not any(self.__dict__.values())

    def to_url(self) -> str:
        """Generates URL query string from current options.

        Returns:
            URL-encoded query string (without leading ?)
        """
        return "&".join([f"${key}={value}" for (key, value) in self])

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        """Yields non-empty query options as key-value pairs."""
        for k, v in self.__dict__.items():
            if not v:
                continue
            if k in ("select", "expand"):
                yield k, ",".join(v)
            elif k == "custom":
                yield from self.custom.items()
            else:
                yield k, str(v)
