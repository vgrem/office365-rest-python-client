"""Migration manifest — the persisted plan of items to move.

The manifest is the "what to migrate": a serializable list of
:class:`MigrationItem` (source/dest path, size, type). It is produced by
enumerating a :class:`DataSource` and persisted as JSON so a run can be
planned, audited, and resumed.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Iterator, List, Optional

from office365.migration.base import ItemStatus, MigrationItem, item_from_dict, item_to_dict

if TYPE_CHECKING:
    from office365.runtime.operations import Progress


class Manifest:
    """A serializable plan of ``MigrationItem`` units."""

    def __init__(self, items: Optional[List[MigrationItem]] = None) -> None:
        self._items: List[MigrationItem] = list(items or [])

    @classmethod
    def from_source(
        cls,
        source,
        progress: Optional[Callable[["Progress"], None]] = None,
    ) -> "Manifest":
        """Enumerate a source into a manifest (with per-item progress)."""
        return cls(source.list_items(progress))

    def add(self, item: MigrationItem) -> "Manifest":
        self._items.append(item)
        return self

    @property
    def items(self) -> List[MigrationItem]:
        return self._items

    @property
    def pending(self) -> List[MigrationItem]:
        return [i for i in self._items if i.status == ItemStatus.PENDING]

    @property
    def failed(self) -> List[MigrationItem]:
        return [i for i in self._items if i.status == ItemStatus.FAILED]

    def by_dest(self) -> dict[str, MigrationItem]:
        return {i.dest_path: i for i in self._items}

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[MigrationItem]:
        return iter(self._items)

    def save(self, path: str | Path) -> None:
        """Persist the manifest as a JSON array of items."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump([item_to_dict(i) for i in self._items], f, indent=2)

    @classmethod
    def load(cls, path: str | Path) -> "Manifest":
        """Load a manifest previously persisted with :meth:`save`."""
        with open(path, "r", encoding="utf-8") as f:
            return cls([item_from_dict(d) for d in json.load(f)])
