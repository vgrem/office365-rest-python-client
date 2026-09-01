"""Generic parallel execution — run a worker across tasks on a thread pool.

Centralizes the thread-pool + per-worker context + shared rate-limiting +
result/error contract so callers don't re-implement it (parallel batch
execution, the migration uploader, ...). Each worker thread lazily creates one
context via ``context_factory`` (e.g. a ``ClientContext.clone``) and, when a
shared :class:`RateLimiter` is given, binds it so the whole fleet paces as a
group on ``Retry-After`` / ``X-SharePointHealthScore``.
"""

from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TYPE_CHECKING, Any, Callable, Iterable, List, Optional

from office365.runtime.http.throttling import RateLimiter

if TYPE_CHECKING:
    from office365.runtime.client_runtime_context import ClientRuntimeContext


def run_parallel(
    worker: Callable[[Optional["ClientRuntimeContext"], Any], Any],
    tasks: Iterable[Any],
    *,
    concurrency: int = 4,
    context_factory: Optional[Callable[[], Optional["ClientRuntimeContext"]]] = None,
    limiter: Optional[RateLimiter] = None,
    progress: Optional[Callable[[Any], None]] = None,
    on_error: Optional[Callable[[Any, Exception], Any]] = None,
) -> List[Any]:
    """Run ``worker(context, task)`` for each task on a thread pool.

    Args:
        worker: Callable invoked once per task with the worker's context (a
          lazily-created per-thread context from ``context_factory``, or None)
          and the task payload.
        tasks: Iterable of task payloads (results are returned in this order).
        concurrency: Maximum number of concurrent worker threads.
        context_factory: Optional zero-arg callable returning a context for each
          worker thread (created once per thread and reused). When a limiter is
          given it is bound to every produced context.
        limiter: Optional shared :class:`RateLimiter` for fleet pacing; when
          ``context_factory`` is given one is created automatically.
        progress: Optional hook fired per completed task with a ``Progress``
          snapshot (``done``/``total``).
        on_error: Optional ``(task, error) -> fallback`` handler; when absent a
          task failure re-raises from the pool.

    Returns:
        Worker results in input order (a failed task yields its ``on_error``
        fallback, or raises).
    """
    tasks = list(tasks)
    if not tasks:
        return []

    if limiter is None and context_factory is not None:
        limiter = RateLimiter()
    results: List[Any] = [None] * len(tasks)
    local = threading.local()
    lock = threading.Lock()
    done = {"count": 0}

    def _context() -> Optional["ClientRuntimeContext"]:
        ctx = getattr(local, "context", None)
        if ctx is None and callable(context_factory):
            ctx = context_factory()
            if ctx is not None and limiter is not None:
                limiter.bind(ctx)
            local.context = ctx
        return ctx

    def _run(index: int, task: Any) -> None:
        try:
            results[index] = worker(_context(), task)
        except Exception as e:  # noqa: BLE001 — per-task errors handled by on_error
            if callable(on_error):
                results[index] = on_error(task, e)
            else:
                raise
        finally:
            with lock:
                done["count"] += 1
                n = done["count"]
        if callable(progress):
            from office365.runtime.operations import Progress

            progress(Progress(done=n, total=len(tasks), stage="parallel"))

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(_run, index, task) for index, task in enumerate(tasks)]
        for future in as_completed(futures):
            future.result()
    return results
