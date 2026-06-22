"""CSV exporter for ClientObjectCollection — reuses .select() + .expand()."""

from __future__ import annotations

import csv
from typing import IO, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject
    from office365.runtime.client_object_collection import ClientObjectCollection


class CollectionCsvWriter:
    """Write collection items to CSV using query_options.select + .expand.

    Plain select fields (e.g. ``"displayName"``) produce one column.
    Dotted select fields (e.g. ``"members/displayName"``) walk into an
    expanded navigation property — one CSV row is emitted per child item.

    Usage:
        >>> client.teams.get_all() \\
        ...     .select(["displayName", "members/displayName", "members/email"]) \\
        ...     .expand(["members"]) \\
        ...     .to_csv(f) \\
        ...     .execute_query()
    """

    def __init__(self, collection: ClientObjectCollection, file: IO) -> None:
        self._collection: ClientObjectCollection = collection
        self._file: IO = file

    def write(self) -> None:
        items: list[ClientObject] = list(self._collection)
        if not items:
            return

        select: list[str] = self._collection.query_options.select
        expand: set[str] = set(self._collection.query_options.expand)

        plain: list[str] = [f for f in select if "/" not in f]
        dotted: list[list[str]] = [f.split("/", 1) for f in select if "/" in f]

        w = csv.writer(self._file)
        w.writerow(select)

        for item in items:
            children: list[dict[str, Any]] | list[ClientObject] = self._resolve_children(item, dotted, expand)
            base = [str(item.properties.get(k, "")) for k in plain]
            for child in children:
                row = list(base)
                for _nav, prop in dotted:
                    row.append(self._child_val(child, prop))
                w.writerow(row)

    @staticmethod
    def _resolve_children(
        item: ClientObject,
        dotted: list[list[str]],
        expand: set[str],
    ) -> list[dict[str, Any]] | list[ClientObject]:
        for nav, _ in dotted:
            if nav not in expand:
                continue
            raw: Any = item.properties.get(nav)
            if raw is None:
                return [{}]
            if hasattr(raw, "_data"):
                return list(raw._data) or [{}]
            return [raw]
        return [{}]

    @staticmethod
    def _child_val(child: Any, key: str) -> str:
        """Read a property from a child item that may be a ClientObject or dict."""
        if isinstance(child, dict):
            return str(child.get(key, ""))
        return str(child.properties.get(key, ""))
