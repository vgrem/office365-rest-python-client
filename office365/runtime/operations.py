"""Progress reporting for long-running operations.

A structured ``Progress`` payload is passed to an optional ``progress`` hook
(``ProgressCallback``) as chunks, pages, or files complete — the same pattern
as azure-storage's ``progress_hook`` or boto3's ``Callback``, adapted to this
library's deferred execution model: hooks fire during ``execute_query()``.
"""

from __future__ import annotations

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
