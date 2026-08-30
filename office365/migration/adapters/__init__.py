"""Source/target adapters for the migration runner.

A migration moves items from a :class:`DataSource` to a :class:`DataTarget`
through a canonical form (bytes for files, dict records for tabular data).
Adapters implement this small contract, so the runner is platform-agnostic —
SharePoint, the filesystem, and (later) S3 / PostgreSQL / Kafka all plug in here.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Iterable, List, Optional

from office365.migration.base import ConflictResolution, MigrationItem

if TYPE_CHECKING:
    from office365.runtime.operations import Progress

MigrationProgress = Optional[Callable[["Progress"], None]]


class DataSource(ABC):
    """Reads migration items from a source."""

    @abstractmethod
    def list_items(self, progress: MigrationProgress = None) -> List[MigrationItem]:
        """Enumerate the items to migrate (with per-item progress)."""

    @abstractmethod
    def read(self, item: MigrationItem) -> object:
        """Read the payload for an item (bytes for files, dict for records)."""

    @abstractmethod
    def checksum(self, item: MigrationItem) -> str:
        """Content hash of an item, used for idempotency and verification."""


class DataTarget(ABC):
    """Writes migration items to a target."""

    @abstractmethod
    def exists(self, item: MigrationItem) -> bool:
        """Whether the item's destination already exists."""

    @abstractmethod
    def write(self, item: MigrationItem, payload: object) -> None:
        """Write the item's payload to its destination."""

    @abstractmethod
    def list_paths(self) -> Iterable[str]:
        """Return all destination paths present on the target (for verification)."""

    @abstractmethod
    def checksum(self, item: MigrationItem) -> str:
        """Content hash of an item already on the target."""


def resolve_dest(item: MigrationItem, target: DataTarget, conflict: ConflictResolution) -> str:
    """Resolve a destination path honoring the conflict-resolution policy.

    ``SKIP`` keeps the original dest (the caller decides whether to skip);
    ``OVERWRITE`` and ``RENAME`` return the effective destination (RENAME appends
    a numeric suffix while the name collides).
    """
    dest = item.dest_path
    if conflict != ConflictResolution.RENAME:
        return dest
    probe = MigrationItem(item.source_path, dest, item.size_bytes, item.item_type)
    if not target.exists(probe):
        return dest
    base, dot, ext = dest.rpartition(".")
    counter = 1
    while True:
        candidate = f"{base}-{counter}{dot}{ext}" if dot else f"{base}-{counter}"
        if not target.exists(MigrationItem(item.source_path, candidate, item.size_bytes, item.item_type)):
            return candidate
        counter += 1
