"""Migration runner — executes a manifest against source/target adapters.

Drives the checkpointed, idempotent item loop: reads each item from the source,
writes it to the target honoring the conflict-resolution policy, records the
per-item status in the checkpoint (persisted after each batch), and collects
:class:`MigrationStats`. Interruptions (pause/cancel) stop cleanly at the next
batch boundary and can be resumed from the checkpoint.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Callable, Iterable, Optional

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
        checkpoint_path: Optional[str | Path] = None,
        progress: Optional[Callable[["Progress"], None]] = None,
        stop_event: Optional[Callable[[], bool]] = None,
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

            processed = stats.success + stats.skipped + stats.errors
            if callable(progress):
                from office365.runtime.operations import Progress

                progress(
                    Progress(
                        done=processed,
                        total=stats.total,
                        stage="migrating",
                        items=[item],
                    )
                )
            if checkpoint_path is not None and (index + 1) % options.batch_size == 0:
                checkpoint.save(checkpoint_path)

        _call_optional(target, "commit")

        if checkpoint.phase != MigrationPhase.PAUSED:
            checkpoint.phase = MigrationPhase.COMPLETED if stats.errors == 0 else MigrationPhase.COMPLETED_WITH_ERRORS
        if checkpoint_path is not None:
            checkpoint.save(checkpoint_path)
        _call_optional(source, "close")
        _call_optional(target, "close")
        return stats

    @staticmethod
    def _migrate(source, target: DataTarget, item: MigrationItem, options: MigrationOptions) -> bool:
        """Move one item; returns ``False`` when skipped by conflict resolution."""
        if options.conflict_resolution == ConflictResolution.SKIP and target.exists(item):
            return False
        dest = resolve_dest(item, target, options.conflict_resolution)
        item.dest_path = dest
        payload = source.read(item)
        target.write(item, payload)
        return True


def _call_optional(adapter, method: str) -> None:
    """Invoke an optional adapter hook (``commit`` / ``close``) if present."""
    hook = getattr(adapter, method, None)
    if callable(hook):
        hook()
