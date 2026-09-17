"""Deferred, streaming, resumable import driver for client-object collections.

An import is expressed as a **stream of chunks** plus a format adapter
(``to_records``) that turns each chunk into plain dict records, so the same
driver serves DataFrames, CSV/JSON streams, or any future source. The driver
carries **no execution knobs** — the caller picks the terminal, mirroring how
mature SDKs separate a deferred handle (BigQuery ``QueryJob``, Azure
``LROPoller``) from its execution:

- :meth:`ImportResult.execute_query` — sequential (one request per item);
- :meth:`ImportResult.execute_batch` — server-side OData batches, optionally
  concurrent;
- ``for collection in import_result:`` — stream chunk by chunk and drive
  execution yourself.

Chunks are queued, executed, and then discarded (``collection.clear()``), so
memory stays bounded regardless of the total item count.

For long-running jobs, pass a ``checkpoint`` (an :class:`ImportCheckpoint` or a
path). The driver persists the committed cursor after each chunk, so an
interrupted run resumes by skipping the already-committed records — at-least-once
(a crash between the server commit and the checkpoint write can replay the last
chunk). With ``on_error="collect"`` a failing chunk is recorded and skipped
instead of aborting the run.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from itertools import islice
from os import PathLike
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterable,
    Iterator,
    Optional,
    Protocol,
    Union,
    cast,
    runtime_checkable,
)

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.operations import OperationStats

if TYPE_CHECKING:
    from office365.runtime.operations import ProgressCallback

ON_ERROR_MODES = ("raise", "collect")


@runtime_checkable
class RecordSink(Protocol):
    """Minimal target contract for :class:`ImportResult` (a queueable collection)."""

    def from_records(self, records: list[dict], progress: "ProgressCallback | None" = None) -> Any:
        """Queue a create per record."""
        ...

    def clear(self) -> Any:
        """Discard queued/loaded entities (keeps memory bounded)."""
        ...


@dataclass
class ImportStats(OperationStats):
    """Outcome of a streaming import (the ``ImportResult.value``).

    Counts are **per invocation**: ``total`` records attempted, ``success``
    committed, ``errors`` skipped under ``on_error="collect"`` (a chunk's size per
    failed chunk). For the overall committed total across resumes, read
    ``ImportCheckpoint.cursor``.
    """

    chunks: int = 0
    duration: float = 0.0
    resumed_from: int = 0  # records already committed by a previous run

    def summary(self) -> str:
        resumed = f" (resumed at {self.resumed_from:,})" if self.resumed_from else ""
        return (
            f"Imported {self.success:,}/{self.total:,} item(s) "
            f"in {self.chunks} chunk(s) over {self.duration:.1f}s{resumed}"
        )


@dataclass
class ImportCheckpoint:
    """Persisted run state enabling resume of a streaming import.

    ``cursor`` is the number of records committed so far (always a chunk
    boundary); a resumed run skips exactly that many leading records. ``failures``
    holds chunk-level errors collected under ``on_error="collect"``.
    """

    cursor: int = 0
    chunks: int = 0
    errors: int = 0
    failures: list[dict] = field(default_factory=list)
    updated_at: str = ""

    def save(self, path: Union[str, PathLike]) -> None:
        """Persist the checkpoint as JSON, atomically (write-then-rename).

        The rename is atomic, so a crash mid-write never leaves a truncated file
        that would break the next resume.
        """
        self.updated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        target = Path(path)
        tmp = target.with_name(f".{target.name}.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "cursor": self.cursor,
                    "chunks": self.chunks,
                    "errors": self.errors,
                    "failures": self.failures,
                    "updated_at": self.updated_at,
                },
                f,
                indent=2,
            )
        tmp.replace(target)

    @classmethod
    def load(cls, path: Union[str, PathLike]) -> "ImportCheckpoint":
        """Load a checkpoint previously persisted with :meth:`save`."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(
            cursor=int(data.get("cursor", 0)),
            chunks=int(data.get("chunks", 0)),
            errors=int(data.get("errors", 0)),
            failures=list(data.get("failures", [])),
            updated_at=data.get("updated_at", ""),
        )


@runtime_checkable
class CheckpointStore(Protocol):
    """Persistence for :class:`ImportCheckpoint` — pluggable, MSAL-cache style."""

    def load(self) -> ImportCheckpoint:
        """Return the persisted checkpoint (a fresh one when none exists)."""
        ...

    def save(self, checkpoint: ImportCheckpoint) -> None:
        """Persist the checkpoint."""
        ...


class MemoryCheckpointStore:
    """In-memory checkpoint store (the default when no path is given)."""

    def __init__(self, checkpoint: Optional[ImportCheckpoint] = None) -> None:
        self._checkpoint = checkpoint or ImportCheckpoint()

    def load(self) -> ImportCheckpoint:
        return self._checkpoint

    def save(self, checkpoint: ImportCheckpoint) -> None:
        self._checkpoint = checkpoint


class FileCheckpointStore:
    """JSON-file checkpoint store (atomic write-then-rename)."""

    def __init__(self, path: Union[str, PathLike]) -> None:
        self._path = Path(path)

    @property
    def path(self) -> Path:
        return self._path

    def load(self) -> ImportCheckpoint:
        return ImportCheckpoint.load(self._path) if self._path.exists() else ImportCheckpoint()

    def save(self, checkpoint: ImportCheckpoint) -> None:
        checkpoint.save(self._path)


class ImportResult(ClientResult[ImportStats]):
    """Deferred, source-agnostic streaming import driver.

    Args:
        context: The runtime context used to execute.
        collection: The target ``ClientObjectCollection`` (queued via
            ``from_records`` and cleared per chunk).
        chunks: Iterable of source chunks (format-defined).
        to_records: Turns one chunk into plain dict records.
        prepare: Optional once-only setup called with the first chunk (e.g.
            schema/field provisioning); it may execute. Skipped when resuming.
        total: Total items when known upfront (drives the progress hook).
        progress: Optional ``ProgressCallback`` fired per queued chunk.
        checkpoint: Persistence for the run state: a path
            (:class:`FileCheckpointStore`), an :class:`ImportCheckpoint` or
            ``None`` (:class:`MemoryCheckpointStore`), or any
            :class:`CheckpointStore`. Loaded at construction, written after each
            chunk. ``ImportResult.resumed_from`` reports the loaded offset.
        on_error: ``"raise"`` (default) aborts on the first failed chunk;
            ``"collect"`` records the failure (``ImportStats.errors`` +
            ``checkpoint.failures``), skips the chunk, and continues.
        queue: Optional conflict-resolution hook ``queue(records) -> (queued, skipped)``
            that queues the chunk's creates/updates and reports how many records
            were queued and how many were skipped (already present). Defaults to
            ``collection.from_records(records)`` (all created, none skipped).
        dry_run: When True, compute the outcome (and the keyed create/update/skip
            plan) without writing anything — a plan preview.
        dead_letter: Optional JSONL path; each collected chunk failure appends
            ``{"error": ..., "records": [...]}`` for remediation (used with
            ``on_error="collect"``).
    """

    def __init__(
        self,
        context,
        collection: "RecordSink",
        chunks: Iterable[Any],
        *,
        to_records: Callable[[Any], list[dict]],
        prepare: Optional[Callable[[Any], None]] = None,
        before_chunk: Optional[Callable[[Any], None]] = None,
        queue: Optional[Callable[[list[dict]], tuple[int, int]]] = None,
        total: Optional[int] = None,
        progress: Optional["ProgressCallback"] = None,
        checkpoint: Union["ImportCheckpoint", "CheckpointStore", str, PathLike, None] = None,
        on_error: str = "raise",
        dry_run: bool = False,
        dead_letter: Union[str, PathLike, None] = None,
    ) -> None:
        super().__init__(context, ImportStats())
        if on_error not in ON_ERROR_MODES:
            raise ValueError(f"on_error must be one of {ON_ERROR_MODES}, got {on_error!r}")
        self._collection = collection
        self._chunks = iter(chunks)
        self._to_records = to_records
        self._prepare = prepare
        self._before_chunk = before_chunk
        self._queue_fn = queue or self._default_queue
        self._total = total
        self._progress = progress
        self._on_error = on_error
        self._dry_run = dry_run
        self._dead_letter = Path(dead_letter) if dead_letter is not None else None
        self._started_at: Optional[float] = None
        self._store = self._resolve_store(checkpoint)
        self._checkpoint = self._store.load()
        self._progress_base = self._checkpoint.cursor  # records committed before this run
        self.value.resumed_from = self._progress_base

    # ── Terminals ────────────────────────────────────────────────

    def execute_query(self) -> Self:
        """Import sequentially (one request per item)."""
        self._run(lambda: self._context.execute_query())
        return self

    def execute_batch(
        self,
        items_per_batch: int = 100,
        max_batch_bytes: Optional[int] = None,
        concurrency: int = 1,
        success_callback: Optional[Callable[[Any], None]] = None,
    ) -> Self:
        """Import via server-side OData batches (optionally concurrent)."""
        execute_batch = cast(Any, self._context).execute_batch
        self._run(
            lambda: execute_batch(
                items_per_batch=items_per_batch,
                max_batch_bytes=max_batch_bytes,
                concurrency=concurrency,
                success_callback=success_callback,
            )
        )
        return self

    def __iter__(self) -> Iterator["RecordSink"]:
        """Yield the target collection per chunk; the caller executes each chunk.

        The caller is responsible for execution (and its errors); checkpoint
        advancement assumes each yielded chunk was committed successfully.
        """
        self._started_at = time.monotonic()
        for raw, records in self._iter_records():
            if callable(self._before_chunk):
                self._before_chunk(raw)
            queued, _skipped = self._queue(records)
            yield self._collection
            self.value.success += queued
            self._advance(records)
            self._collection.clear()
        self._finish()

    # ── Core ─────────────────────────────────────────────────────

    def _run(self, execute: Callable[[], Any]) -> None:
        """Drive the chunk loop: skip committed records, queue, execute, persist."""
        self._started_at = time.monotonic()
        for raw, records in self._iter_records():
            if callable(self._before_chunk):
                self._before_chunk(raw)
            queued, _skipped = self._queue(records)
            if self._dry_run:
                self.value.success += queued
                self._advance(records)
                self._collection.clear()
                continue
            try:
                execute()
            except Exception as ex:  # noqa: BLE001 — policy decides whether to abort
                self._record_failure(queued, records, ex)
                self._collection.clear()
                if self._on_error != "collect":
                    self._save_checkpoint()  # cursor unchanged — resume retries this chunk
                    raise
                self._advance(records)  # collect: skip the failed chunk, keep going
            else:
                self.value.success += queued
                self._advance(records)
                self._collection.clear()
            self._save_checkpoint()
        self._finish()

    def _iter_records(self) -> Iterator[tuple[Any, list[dict]]]:
        """Yield ``(raw_chunk, records)``, skipping already-committed chunks.

        Commits are whole chunks, so resume skips by the checkpoint's ``chunks``
        count (cheap — no ``to_records`` on committed data). A record-level
        ``cursor`` fallback covers a hand-built checkpoint without a chunk count.
        ``prepare`` runs only on a fresh run (fields already exist when resuming).
        """
        skip_chunks = self._checkpoint.chunks
        skip_records = 0 if skip_chunks else self._checkpoint.cursor
        prepared = skip_chunks > 0 or skip_records > 0
        source = islice(self._chunks, skip_chunks, None) if skip_chunks else self._chunks
        for raw in source:
            records = self._to_records(raw)
            if skip_records:
                if len(records) <= skip_records:
                    skip_records -= len(records)
                    continue
                records = records[skip_records:]
                skip_records = 0
            if not prepared:
                if callable(self._prepare):
                    self._prepare(raw)
                prepared = True
            yield raw, records

    # ── Bookkeeping ──────────────────────────────────────────────

    def _default_queue(self, records: list[dict]) -> tuple[int, int]:
        """Queue every record as a create (no conflict resolution)."""
        if not self._dry_run:
            self._collection.from_records(records)
        return len(records), 0

    def _queue(self, records: list[dict]) -> tuple[int, int]:
        """Queue a chunk via the conflict-resolution hook; returns (queued, skipped)."""
        from office365.runtime.operations import Progress

        queued, skipped = self._queue_fn(records)
        self.value.total += len(records)
        self.value.skipped += skipped
        if callable(self._progress):
            done = self._progress_base + self.value.total  # overall, across resumes
            self._progress(Progress(done=done, total=self._total, stage="importing"))
        return queued, skipped

    def _advance(self, records: list[dict]) -> None:
        self.value.chunks += 1
        self._checkpoint.cursor += len(records)
        self._checkpoint.chunks += 1

    def _record_failure(self, count: int, records: list[dict], error: Exception) -> None:
        self.value.errors += count
        self._checkpoint.errors += count
        self._checkpoint.failures.append({"records": count, "error": str(error)})
        if self._dead_letter is not None:
            self._dead_letter.parent.mkdir(parents=True, exist_ok=True)
            with open(self._dead_letter, "a", encoding="utf-8") as f:
                f.write(json.dumps({"error": str(error), "records": records}, default=str) + "\n")

    def _finish(self) -> None:
        if self._started_at is not None:
            self.value.duration = time.monotonic() - self._started_at

    @staticmethod
    def _resolve_store(
        checkpoint: Union["ImportCheckpoint", "CheckpointStore", str, PathLike, None],
    ) -> "CheckpointStore":
        if checkpoint is None:
            return MemoryCheckpointStore()
        if isinstance(checkpoint, ImportCheckpoint):
            return MemoryCheckpointStore(checkpoint)
        if isinstance(checkpoint, CheckpointStore):
            return checkpoint
        return FileCheckpointStore(checkpoint)

    def _save_checkpoint(self) -> None:
        self._store.save(self._checkpoint)

    # ── State ────────────────────────────────────────────────────

    @property
    def checkpoint(self) -> ImportCheckpoint:
        """The live run state (cursor/errors/failures), updated after each chunk."""
        return self._checkpoint

    @property
    def resumed_from(self) -> int:
        """Records already committed by a previous run (``0`` when fresh)."""
        return self._progress_base
