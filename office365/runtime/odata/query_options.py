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

    _OPTIONS = {
        "select": "select",
        "expand": "expand",
        "filter": "filter",
        "order_by": "orderby",
        "top": "top",
        "skip": "skip",
    }
    _WIRE_NAMES = frozenset(_OPTIONS.values())

    def to_url(self) -> str:
        """Generates URL query string from current options.

        In a request every option is spelled the way the specification spells it:
        ``order_by`` is sent as ``$orderby``, because sending the Python name is
        not refused — the service answers ``200`` and ignores the option, so the
        caller silently loses the ordering.

        The six names above are always ``$``-prefixed, so a caller who spells one
        of them as a custom key still gets the URL the service expects. Any other
        custom key is emitted verbatim: it is the caller's vocabulary, not ours
        (``token`` is the OneDrive/SharePoint delta cursor).

        Returns:
            URL-encoded query string (without leading ?)
        """
        parts = []
        for key, value in self:
            prefix = "$" if key in self._WIRE_NAMES else ""
            parts.append(f"{prefix}{key}={value}")
        return "&".join(parts)

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        """Yields non-empty query options as key-value pairs, under their wire names."""
        for k, v in self.__dict__.items():
            if not v:
                continue
            if k in ("select", "expand"):
                yield self._OPTIONS[k], ",".join(v)
            elif k == "custom":
                yield from self.custom.items()
            else:
                yield self._OPTIONS[k], str(v)

    def apply_to(self, target) -> None:
        """Forward ``$select`` / ``$expand`` onto a collection-like target about to load.

        Used by recursive scan helpers so the fluent ``.select(...)`` /
        ``.expand(...)`` applied to their returned collection reaches every
        request they issue (the scan reads the options at execution time).

        Args:
            target: A collection exposing ``select`` / ``expand`` (duck-typed).
        """
        if self.select:
            target.select(list(self.select))
        if self.expand:
            target.expand(list(self.expand))
