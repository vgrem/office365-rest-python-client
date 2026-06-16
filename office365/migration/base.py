"""
office365.migration.base
~~~~~~~~~~~~~~~~~~~~~~~~
Shared types, enums, and the MigrationQuery base class.

MigrationQuery extends ClientQuery so all migration operations
plug into the existing deferred execution pipeline:
    operation.execute_query()
    operation.execute_query_retry()
    operation.after_execute(callback)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

# ── Enums ─────────────────────────────────────────────────────────────────────


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


# ── Value types ───────────────────────────────────────────────────────────────


@dataclass
class MigrationItem:
    """Unit of work flowing through the migration pipeline."""

    source_path: str
    dest_path: str
    size_bytes: int = 0
    item_type: str = "file"
    status: str = "pending"
    error: Exception | None = None


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
    preserve_timestamps: bool = True
    preserve_permissions: bool = False
    preserve_versions: bool = False
    include_patterns: list[str] = field(default_factory=list)
    exclude_patterns: list[str] = field(default_factory=list)
    batch_size: int = 100
