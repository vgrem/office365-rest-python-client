"""
Shared types and enums for the migration toolkit.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from enum import Enum


class ConflictResolution(str, Enum):
    SKIP = "skip"
    OVERWRITE = "overwrite"
    RENAME = "rename"


class MigrationMode(str, Enum):
    FULL = "full"
    INCREMENTAL = "incremental"
    UPSERT = "upsert"


class ExportFormat(str, Enum):
    FILESYSTEM = "filesystem"
    PARQUET = "parquet"
    CSV = "csv"
    JSON = "json"
    DELTA = "delta"


class ItemStatus(str, Enum):
    """Per-item status, persisted in the checkpoint for resumable migrations."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    SKIPPED = "skipped"
    FAILED = "failed"


class MigrationPhase(str, Enum):
    """Lifecycle of a migration job (scan -> plan -> run -> monitor).

    ``paused`` / ``failed`` / ``cancelled`` all retain a persisted checkpoint, so
    the job can be resumed from where it stopped.
    """

    CREATED = "created"
    ASSESSING = "assessing"
    PLANNING = "planning"
    RUNNING = "running"
    PAUSED = "paused"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class MigrationItem:
    """Unit of work flowing through the migration pipeline."""

    source_path: str
    dest_path: str
    size_bytes: int = 0
    item_type: str = "file"
    status: ItemStatus = ItemStatus.PENDING
    error: str | None = None
    modified: str | None = None  # source last-modified (ISO-8601), for incremental


@dataclass
class MigrationStats:
    total: int = 0
    success: int = 0
    skipped: int = 0
    errors: int = 0
    bytes_transferred: int = 0

    def summary(self) -> str:
        mb = self.bytes_transferred / 1024 / 1024
        return (
            f"Total: {self.total} | Success: {self.success} | "
            f"Skipped: {self.skipped} | Errors: {self.errors} | "
            f"Transferred: {mb:.1f}MB"
        )


@dataclass
class MigrationOptions:
    conflict_resolution: ConflictResolution = ConflictResolution.SKIP
    incremental: bool = False  # skip items whose target is at least as new as the source
    preserve_timestamps: bool = True
    preserve_permissions: bool = False
    preserve_versions: bool = False
    include_patterns: list[str] = field(default_factory=list)
    exclude_patterns: list[str] = field(default_factory=list)
    batch_size: int = 100
    concurrency: int = 1  # parallel workers for bulk file upload / batched writes


def item_to_dict(item: MigrationItem) -> dict:
    """Serialize a ``MigrationItem`` to a JSON-safe dict (enum/error by value)."""
    data = asdict(item)
    data["status"] = item.status.value
    data["error"] = str(item.error) if item.error else None
    return data


def item_from_dict(data: dict) -> MigrationItem:
    """Rebuild a ``MigrationItem`` (missing fields fall back to dataclass defaults)."""
    kwargs = {f.name: data[f.name] for f in fields(MigrationItem) if f.name in data}
    if "status" in kwargs:
        kwargs["status"] = ItemStatus(kwargs["status"])
    return MigrationItem(**kwargs)
