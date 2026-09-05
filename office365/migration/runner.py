"""Migration runner — executes a manifest against source/target adapters.

Drives the checkpointed, idempotent item loop: reads each item from the source,
writes it to the target honoring the conflict-resolution policy, records the
per-item status in the checkpoint (persisted after each batch), and collects
:class:`MigrationStats`. Interruptions (pause/cancel) stop cleanly at the next
batch boundary and can be resumed from the checkpoint.

With ``MigrationOptions.concurrency > 1`` and a target that supports a bulk
``write_many`` hook (e.g. the SharePoint library target), items are uploaded in
parallel chunks — file bytes can't ride an OData batch, so throughput comes from
concurrency, paced by a shared rate limiter.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Callable, Iterable

from office365.migration._util import emit_progress
from office365.migration.adapters import DataTarget, resolve_dest
from office365.migration.base import (
    ConflictResolution,
    ItemStatus,
    MigrationItem,
    MigrationOptions,
    MigrationPhase,
    MigrationStats,
)
from office365.migration.checkpoint import Checkpoint

if TYPE_CHECKING:
    from office365.runtime.operations import Progress


class MigrationRunner:
    """Executes migration items between a source and a target adapter."""

    def run(
        self,
        source,
        target: DataTarget,
        items: Iterable[MigrationItem],
        options: MigrationOptions,
        checkpoint: Checkpoint,
        checkpoint_path: str | Path | None = None,
        progress: Callable[["Progress"], None] | None = None,
        stop_event: Callable[[], bool] | None = None,
    ) -> MigrationStats:
        parallel = (
            options.concurrency > 1
            and hasattr(target, "write_many")
            and options.conflict_resolution != ConflictResolution.RENAME
        )
        if parallel:
            stats = self._run_parallel(source, target, items, options, checkpoint, checkpoint_path, progress, stop_event)
        else:
            stats = self._run_sequential(
                source, target, items, options, checkpoint, checkpoint_path, progress, stop_event
            )
        _call_optional(target, "commit", options)

        if checkpoint.phase != MigrationPhase.PAUSED:
            checkpoint.phase = MigrationPhase.COMPLETED if stats.errors == 0 else MigrationPhase.COMPLETED_WITH_ERRORS
        if checkpoint_path is not None:
            checkpoint.save(checkpoint_path)
        _call_optional(source, "close")
        _call_optional(target, "close")
        return stats

    def _run_sequential(
        self,
        source,
        target: DataTarget,
        items: Iterable[MigrationItem],
        options: MigrationOptions,
        checkpoint: Checkpoint,
        checkpoint_path: str | Path | None,
        progress: Callable[["Progress"], None] | None,
        stop_event: Callable[[], bool] | None,
    ) -> MigrationStats:
        stats = MigrationStats(total=0)
        for index, item in enumerate(items):
            stats.total += 1
            status = checkpoint.status_of(item)
            if status in (ItemStatus.DONE, ItemStatus.SKIPPED):
                stats.skipped += 1
                continue
            if callable(stop_event) and stop_event():
                checkpoint.phase = MigrationPhase.PAUSED
                break
            checkpoint.record(item, ItemStatus.IN_PROGRESS)
            try:
                if self._migrate(source, target, item, options):
                    checkpoint.record(item, ItemStatus.DONE)
                    stats.success += 1
                    stats.bytes_transferred += item.size_bytes
                else:
                    checkpoint.record(item, ItemStatus.SKIPPED)
                    stats.skipped += 1
            except Exception as e:  # noqa: BLE001 — per-item errors are captured, not fatal
                item.error = str(e)
                checkpoint.record(item, ItemStatus.FAILED)
                stats.errors += 1
            self._report_progress(progress, stats, item)
            if checkpoint_path is not None and (index + 1) % options.batch_size == 0:
                checkpoint.save(checkpoint_path)
        return stats

    def _run_parallel(
        self,
        source,
        target: DataTarget,
        items: Iterable[MigrationItem],
        options: MigrationOptions,
        checkpoint: Checkpoint,
        checkpoint_path: str | Path | None,
        progress: Callable[["Progress"], None] | None,
        stop_event: Callable[[], bool] | None,
    ) -> MigrationStats:
        stats = MigrationStats(total=0)
        chunk: list[MigrationItem] = []

        def _flush() -> None:
            if not chunk:
                return
            payloads = [source.read(item) for item in chunk]
            failures = target.write_many(chunk, payloads, concurrency=options.concurrency)
            failed = {path: error for path, error in failures}
            for item in chunk:
                if item.dest_path in failed:
                    item.error = failed[item.dest_path]
                    checkpoint.record(item, ItemStatus.FAILED)
                    stats.errors += 1
                else:
                    checkpoint.record(item, ItemStatus.DONE)
                    stats.success += 1
                    stats.bytes_transferred += item.size_bytes
                self._report_progress(progress, stats, item)
            chunk.clear()
            if checkpoint_path is not None:
                checkpoint.save(checkpoint_path)

        for _index, item in enumerate(items):
            stats.total += 1
            status = checkpoint.status_of(item)
            if status in (ItemStatus.DONE, ItemStatus.SKIPPED):
                stats.skipped += 1
                continue
            if callable(stop_event) and stop_event():
                checkpoint.phase = MigrationPhase.PAUSED
                break
            checkpoint.record(item, ItemStatus.IN_PROGRESS)
            if options.incremental and _target_up_to_date(source, target, item):
                checkpoint.record(item, ItemStatus.SKIPPED)
                stats.skipped += 1
                continue
            if options.conflict_resolution == ConflictResolution.SKIP and target.exists(item):
                checkpoint.record(item, ItemStatus.SKIPPED)
                stats.skipped += 1
                continue
            chunk.append(item)
            if len(chunk) >= options.batch_size:
                _flush()
        _flush()
        return stats

    @staticmethod
    def _report_progress(progress, stats: MigrationStats, item: MigrationItem) -> None:
        processed = stats.success + stats.skipped + stats.errors
        emit_progress(progress, done=processed, total=stats.total, stage="migrating", items=[item])

    @staticmethod
    def _migrate(source, target: DataTarget, item: MigrationItem, options: MigrationOptions) -> bool:
        """Move one item; returns ``False`` when skipped (conflict/incremental)."""
        if options.incremental and _target_up_to_date(source, target, item):
            return False
        if options.conflict_resolution == ConflictResolution.SKIP and target.exists(item):
            return False
        dest = resolve_dest(item, target, options.conflict_resolution)
        item.dest_path = dest
        payload = source.read(item)
        target.write(item, payload)
        return True


def _target_up_to_date(source, target: DataTarget, item: MigrationItem) -> bool:
    """Incremental check: skip when the target is at least as new as the source."""
    if item.modified is None:
        return False
    target_modified = getattr(target, "modified", None)
    if not callable(target_modified) or not target.exists(item):
        return False
    target_value = target_modified(item)
    return target_value is not None and str(target_value) >= item.modified


def _call_optional(adapter, method: str, *args) -> None:
    """Invoke an optional adapter hook (``commit`` / ``close``) if present."""
    hook = getattr(adapter, method, None)
    if callable(hook):
        hook(*args)
