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
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Iterable, Iterator, Optional, Union, cast

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.operations import OperationStats

if TYPE_CHECKING:
    from office365.runtime.client_object_collection import ClientObjectCollection
    from office365.runtime.operations import ProgressCallback

ON_ERROR_MODES = ("raise", "collect")


@dataclass
class ImportStats(OperationStats):
    """Outcome of a streaming import (the ``ImportResult.value``).

    ``total`` is the records attempted, ``success`` the records committed,
    ``errors`` the records skipped under ``on_error="collect"`` (a chunk's size
    per failed chunk).
    """

    chunks: int = 0
    duration: float = 0.0

    def summary(self) -> str:
        return f"Imported {self.success:,}/{self.total:,} item(s) in {self.chunks} chunk(s) over {self.duration:.1f}s"


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
        """Persist the checkpoint as JSON."""
        self.updated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with open(path, "w", encoding="utf-8") as f:
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
        checkpoint: An :class:`ImportCheckpoint` or a path to persist/resume
            from. A path is loaded when it exists and written after each chunk.
        on_error: ``"raise"`` (default) aborts on the first failed chunk;
            ``"collect"`` records the failure (``ImportStats.errors`` +
            ``checkpoint.failures``), skips the chunk, and continues.
    """

    def __init__(
        self,
        context,
        collection: "ClientObjectCollection",
        chunks: Iterable[Any],
        *,
        to_records: Callable[[Any], list[dict]],
        prepare: Optional[Callable[[Any], None]] = None,
        total: Optional[int] = None,
        progress: Optional["ProgressCallback"] = None,
        checkpoint: Union["ImportCheckpoint", str, PathLike, None] = None,
        on_error: str = "raise",
    ) -> None:
        super().__init__(context, ImportStats())
        if on_error not in ON_ERROR_MODES:
            raise ValueError(f"on_error must be one of {ON_ERROR_MODES}, got {on_error!r}")
        self._collection = collection
        self._chunks = iter(chunks)
        self._to_records = to_records
        self._prepare = prepare
        self._total = total
        self._progress = progress
        self._on_error = on_error
        self._started_at: Optional[float] = None
        self._checkpoint_path, self._checkpoint = self._resolve_checkpoint(checkpoint)

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

    def __iter__(self) -> Iterator["ClientObjectCollection"]:
        """Yield the target collection per chunk; the caller executes each chunk.

        The caller is responsible for execution (and its errors); checkpoint
        advancement assumes each yielded chunk was committed successfully.
        """
        self._started_at = time.monotonic()
        for _raw, records in self._iter_records():
            self._queue(records)
            yield self._collection
            self._commit(records)
            self._collection.clear()
        self._finish()

    # ── Core ─────────────────────────────────────────────────────

    def _run(self, execute: Callable[[], Any]) -> None:
        """Drive the chunk loop: skip committed records, queue, execute, persist."""
        self._started_at = time.monotonic()
        for _raw, records in self._iter_records():
            self._queue(records)
            try:
                execute()
            except Exception as ex:  # noqa: BLE001 — policy decides whether to abort
                self._record_failure(records, ex)
                self._collection.clear()
                if self._on_error != "collect":
                    self._save_checkpoint()  # cursor unchanged — resume retries this chunk
                    raise
                self._advance(records)  # collect: skip the failed chunk, keep going
            else:
                self.value.success += len(records)
                self._advance(records)
                self._collection.clear()
            self._save_checkpoint()
        self._finish()

    def _iter_records(self) -> Iterator[tuple[Any, list[dict]]]:
        """Yield ``(raw_chunk, records)``, skipping already-committed records.

        The checkpoint cursor is always a chunk boundary, so whole chunks are
        skipped; ``prepare`` runs only on a fresh run (fields already exist when
        resuming).
        """
        skip = self._checkpoint.cursor
        prepared = skip > 0
        for raw in self._chunks:
            records = self._to_records(raw)
            if skip:
                if len(records) <= skip:
                    skip -= len(records)
                    continue
                records = records[skip:]
                skip = 0
            if not prepared:
                if callable(self._prepare):
                    self._prepare(raw)
                prepared = True
            yield raw, records

    # ── Bookkeeping ──────────────────────────────────────────────

    def _queue(self, records: list[dict]) -> None:
        from office365.runtime.operations import Progress

        self._collection.from_records(records)
        self.value.total += len(records)
        if callable(self._progress):
            self._progress(Progress(done=self.value.total, total=self._total, stage="importing"))

    def _commit(self, records: list[dict]) -> None:
        self.value.success += len(records)
        self._advance(records)

    def _advance(self, records: list[dict]) -> None:
        self.value.chunks += 1
        self._checkpoint.cursor += len(records)
        self._checkpoint.chunks += 1

    def _record_failure(self, records: list[dict], error: Exception) -> None:
        self.value.errors += len(records)
        self._checkpoint.errors += len(records)
        self._checkpoint.failures.append({"records": len(records), "error": str(error)})

    def _finish(self) -> None:
        if self._started_at is not None:
            self.value.duration = time.monotonic() - self._started_at

    def _resolve_checkpoint(
        self, checkpoint: Union["ImportCheckpoint", str, PathLike, None]
    ) -> tuple[Optional[Path], ImportCheckpoint]:
        if checkpoint is None:
            return None, ImportCheckpoint()
        if isinstance(checkpoint, ImportCheckpoint):
            return None, checkpoint
        path = Path(checkpoint)
        return path, (ImportCheckpoint.load(path) if path.exists() else ImportCheckpoint())

    def _save_checkpoint(self) -> None:
        if self._checkpoint_path is not None:
            self._checkpoint.save(self._checkpoint_path)
