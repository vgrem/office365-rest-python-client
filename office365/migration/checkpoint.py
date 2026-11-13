"""Migration checkpoint — the persisted run state enabling resume.

A checkpoint records the job's phase, an optional source watermark (for
incremental migrations), and the per-item status for every item in the
manifest. The runner persists it after each batch, so an interrupted or failed
run can resume by re-driving only ``pending`` / ``failed`` / ``in_progress``
items — a checkpointed, idempotent, at-least-once migration.

An item is identified by its **source** identity (``source_id``, or the source
path when the adapter reports none), not by the target path: a resume has to
recognise what it already took from the source even when the target path was
resolved differently on the second run (`--rename`, collision suffixes).

The file extension picks the store: ``.sqlite`` / ``.sqlite3`` / ``.db`` is a
SQLite ledger, anything else is JSON. Both are written as one atomic unit; the
ledger additionally lets an operator watch a live run
(``select status, count(*) from item group by 1``) and is the place session
state and the old→new map will live. It is not a speed win — a row costs more
than a line of JSON — so choose it for the single-transaction write and the
queryable view, not for throughput.
"""

from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from office365.migration.base import ItemStatus, MigrationItem, MigrationPhase
from office365.runtime.converters.scalars import utc_now_iso
from office365.runtime.persistence import atomic_write_json, read_json

#: An extension that means "ledger". Anything else keeps the JSON a run already had.
_SQLITE_SUFFIXES = frozenset({".sqlite", ".sqlite3", ".db"})
_SCHEMA = """
CREATE TABLE IF NOT EXISTS run (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    run_id TEXT NOT NULL,
    phase TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    source_watermark TEXT
);
CREATE TABLE IF NOT EXISTS item (identity TEXT PRIMARY KEY, status TEXT NOT NULL);
"""


def _identity(item: MigrationItem) -> str:
    return item.source_id or item.source_path


def _sqlite(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path, timeout=30)
    connection.execute("PRAGMA journal_mode=WAL")  # a reader is not blocked by the writer
    connection.executescript(_SCHEMA)
    return connection


@dataclass
class Checkpoint:
    """Run-state snapshot for a migration job."""

    run_id: str
    phase: MigrationPhase = MigrationPhase.CREATED
    updated_at: str = ""
    source_watermark: str | None = None
    items: dict[str, str] = field(default_factory=dict)  # source identity -> ItemStatus.value

    @classmethod
    def create(cls, run_id: str | None = None) -> "Checkpoint":
        return cls(
            run_id=run_id or uuid.uuid4().hex[:12],
            phase=MigrationPhase.CREATED,
            updated_at=utc_now_iso(),
        )

    def status_of(self, item: MigrationItem) -> ItemStatus:
        return ItemStatus(self.items.get(_identity(item), ItemStatus.PENDING.value))

    def record(self, item: MigrationItem, status: ItemStatus) -> None:
        self.items[_identity(item)] = status.value
        item.status = status
        self.updated_at = utc_now_iso()

    def done_count(self) -> int:
        return sum(1 for v in self.items.values() if v == ItemStatus.DONE.value)

    def save(self, path: str | Path) -> None:
        """Persist the checkpoint, atomically, as JSON or as a SQLite ledger.

        A crash mid-save never leaves a partial state, so a resumed run always
        reads either the previous or the complete new checkpoint: JSON writes a
        temp file, flushes it and renames; the ledger writes one transaction.

        The ledger is rewritten whole rather than diffed. A checkpoint is one row
        per item, so this is a bulk insert (and a run's item count is bounded by
        its manifest), and writing memory as-is is what keeps a caller that put
        something into ``items`` by hand from being silently dropped.
        """
        path = Path(path)
        if path.suffix.lower() in _SQLITE_SUFFIXES:
            connection = _sqlite(path)
            try:
                with connection:
                    connection.execute("DELETE FROM item")
                    connection.executemany("INSERT INTO item(identity, status) VALUES (?, ?)", self.items.items())
                    connection.execute(
                        "INSERT INTO run(id, run_id, phase, updated_at, source_watermark) VALUES (1, ?, ?, ?, ?)"
                        " ON CONFLICT(id) DO UPDATE SET run_id = excluded.run_id, phase = excluded.phase,"
                        " updated_at = excluded.updated_at, source_watermark = excluded.source_watermark",
                        (self.run_id, self.phase.value, self.updated_at, self.source_watermark),
                    )
            finally:
                connection.close()
            return
        atomic_write_json(
            path,
            {
                "run_id": self.run_id,
                "phase": self.phase.value,
                "updated_at": self.updated_at,
                "source_watermark": self.source_watermark,
                "items": self.items,
            },
        )

    @classmethod
    def load(cls, path: str | Path) -> "Checkpoint":
        """Load a checkpoint previously persisted with :meth:`save`."""
        path = Path(path)
        if path.suffix.lower() in _SQLITE_SUFFIXES:
            if not path.exists():  # nothing has been written yet: a fresh run, not an error
                return cls.create()
            connection = _sqlite(path)
            try:
                run = connection.execute("SELECT run_id, phase, updated_at, source_watermark FROM run").fetchone()
                items = dict(connection.execute("SELECT identity, status FROM item"))
            finally:
                connection.close()
            if run is None:
                return cls.create()
            return cls(
                run_id=run[0],
                phase=MigrationPhase(run[1]),
                updated_at=run[2],
                source_watermark=run[3],
                items=items,
            )
        data = read_json(path)
        return cls(
            run_id=data["run_id"],
            phase=MigrationPhase(data.get("phase", MigrationPhase.CREATED.value)),
            updated_at=data.get("updated_at", ""),
            source_watermark=data.get("source_watermark"),
            items=data.get("items", {}),
        )
