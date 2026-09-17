"""Progress reporting for long-running operations.

A structured ``Progress`` payload is passed to an optional ``progress`` hook
(``ProgressCallback``) as chunks, pages, or files complete — the same pattern
as azure-storage's ``progress_hook`` or boto3's ``Callback``, adapted to this
library's deferred execution model: hooks fire during ``execute_query()``.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from itertools import count
from typing import Any, Callable, Generic, Optional, Sequence, TypeVar

T_co = TypeVar("T_co", covariant=True)


@dataclass
class Progress(Generic[T_co]):
    """A snapshot of a long-running operation's progress.

    ``T_co`` is the item type carried by ``items`` (e.g. ``Progress[File]``);
    numeric-only operations use ``Progress[Any]``.

    Attributes:
        done: Work completed so far (bytes, items, pages...).
        total: Total work when known; ``None`` for indeterminate operations.
        stage: Human-readable stage, e.g. ``"uploading"``.
        items: The batch of items completed by this step, when the operation
          completes several per step (e.g. a folder scan's files). Treated as
          read-only; ``None`` for single-item or numeric steps — ``done``
          already carries the count. Never the full result set.
    """

    done: int = 0
    total: Optional[int] = None
    stage: str = ""
    items: Optional[Sequence[T_co]] = None

    @property
    def percent(self) -> Optional[float]:
        """Completion percentage (0-100), or ``None`` when total is unknown."""
        if not self.total:
            return None
        return min(100.0, self.done / self.total * 100)


ProgressCallback = Callable[[Progress[Any]], None]


def emit_progress(
    progress: Optional[ProgressCallback],
    *,
    done: int,
    total: Optional[int] = None,
    stage: str = "",
    items: Optional[Sequence[Any]] = None,
) -> None:
    """Invoke a progress hook (if any) with a :class:`Progress` snapshot."""
    if callable(progress):
        progress(Progress(done=done, total=total, stage=stage, items=items))


@dataclass
class OperationStats:
    """Common counters shared by bulk operations (imports, migrations).

    The base carries only the fields every operation can report, so a consumer
    that needs just totals accepts any specialization (``ImportStats``,
    ``MigrationStats``) without a lossy conversion. Specializations add their own
    extras (``chunks``/``duration``, ``bytes_transferred``).
    """

    total: int = 0
    success: int = 0
    skipped: int = 0
    errors: int = 0


class ProgressTracker:
    """Shared emitter that turns operation sub-steps into ``Progress`` snapshots.

    Operations that complete in sub-steps (pages, chunks, files, batches) advance
    a tracker from their ``after_execute`` hooks; it centralizes counting and
    builds a consistent ``Progress`` payload. Thread-safe, so it can be shared
    between worker threads (e.g. ``run_parallel``) and a reporting thread.

    Args:
        progress: Optional ``ProgressCallback`` to invoke per report.
        total: Total work when known upfront (may be set later via ``set_total``).
        stage: The operation stage reported on every snapshot.

    Example:
        >>> tracker = ProgressTracker(callback, total=100, stage="uploading")
        >>> def _chunk_done(return_type):  # registered via after_execute
        ...     tracker.advance(len(return_type.value))
    """

    def __init__(
        self,
        progress: ProgressCallback | None = None,
        *,
        total: Optional[int] = None,
        stage: str = "",
    ) -> None:
        self._callback = progress
        self._total = total
        self._stage = stage
        self._done = 0
        self._lock = threading.Lock()

    @property
    def done(self) -> int:
        return self._done

    @property
    def total(self) -> Optional[int]:
        return self._total

    def set_total(self, total: Optional[int]) -> None:
        """Set (or update) the total; lets late determinate totals be reported."""
        self._total = total

    def report(self, done: int, items=None) -> None:
        """Report an absolute ``done`` count."""
        with self._lock:
            self._done = max(self._done, done)
            done_value = self._done
        self._emit(done_value, items)

    def advance(self, amount: int = 1, items=None) -> None:
        """Advance ``done`` by ``amount`` and report it."""
        with self._lock:
            self._done += amount
            done_value = self._done
        self._emit(done_value, items)

    def _emit(self, done: int, items) -> None:
        if callable(self._callback):
            self._callback(Progress(done=done, total=self._total, stage=self._stage, items=items))


def query_progress_hook(total: int, progress: ProgressCallback, stage: str = "") -> Callable[[Any], None]:
    """Return a hook that reports the completion of each of ``total`` queries.

    Register the returned hook per query via ``context.after_execute(hook)``; as
    the queries complete during ``execute_query()`` a ``Progress`` snapshot is
    emitted (``done`` = queries completed, ``total`` = the fixed count given
    here). Generic by design: the stage is caller-supplied (default empty).

    Usage:
        >>> from office365.runtime.operations import Progress, query_progress_hook
        >>> hook = query_progress_hook(len(records), my_callback)
        >>> for qry in queued_queries:
        ...     context.add_query(qry)
        ...     context.after_execute(hook)
    """
    completed = count(1)

    def _hook(_return_type: Any) -> None:
        progress(Progress(done=next(completed), total=total, stage=stage))

    return _hook
