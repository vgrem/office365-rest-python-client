"""Dedicated worker pool for offloading blocking transport work.

The async API runs blocking ``requests`` calls (and the synchronous
``beforeExecute`` hooks) in a worker thread. By default those go to a
process-wide executor owned by the library rather than the event loop's shared
default pool, so an async app can size the two independently and heavy HTTP work
does not starve other loop callbacks.

The executor is created lazily on first use, so importing the library spawns no
threads. Call :func:`configure_offload_executor` before the first async request
to tune it, or :func:`shutdown_offload_executor` to release its threads.

    from office365.runtime.transport.offload import configure_offload_executor

    configure_offload_executor(max_workers=16)

A transport can bypass the shared pool with its own executor by setting
:attr:`office365.runtime.transport.base.BaseTransport.offload_executor`.
"""

from __future__ import annotations

import asyncio
import contextvars
import functools
import threading
from concurrent.futures import Executor, ThreadPoolExecutor
from typing import Callable, Optional, TypeVar

T = TypeVar("T")

#: Default worker-thread name prefix for the shared offload pool.
_DEFAULT_THREAD_NAME_PREFIX = "office365-offload"

#: Default maximum worker count, mirroring ``ThreadPoolExecutor``:
#: ``min(32, os.cpu_count() + 4)``.
DEFAULT_MAX_WORKERS: Optional[int] = None


class _OffloadPool:
    """Lazily-built, process-wide executor shared by the offload call sites."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._executor: Optional[Executor] = None
        self._max_workers: Optional[int] = DEFAULT_MAX_WORKERS
        self._thread_name_prefix = _DEFAULT_THREAD_NAME_PREFIX

    def configure(self, max_workers: Optional[int], thread_name_prefix: Optional[str]) -> None:
        if max_workers is not None and max_workers < 1:
            raise ValueError("max_workers must be a positive integer or None")
        with self._lock:
            if self._executor is not None:
                raise RuntimeError(
                    "The offload executor has already been created; call "
                    "shutdown_offload_executor() before reconfiguring it."
                )
            self._max_workers = max_workers
            if thread_name_prefix is not None:
                self._thread_name_prefix = thread_name_prefix

    def get(self) -> Executor:
        with self._lock:
            if self._executor is None:
                self._executor = ThreadPoolExecutor(
                    max_workers=self._max_workers,
                    thread_name_prefix=self._thread_name_prefix,
                )
            return self._executor

    def shutdown(self, wait: bool) -> None:
        with self._lock:
            executor = self._executor
            self._executor = None
            self._max_workers = DEFAULT_MAX_WORKERS
            self._thread_name_prefix = _DEFAULT_THREAD_NAME_PREFIX
        if executor is not None:
            executor.shutdown(wait=wait)


_pool = _OffloadPool()


def configure_offload_executor(
    max_workers: Optional[int] = DEFAULT_MAX_WORKERS,
    thread_name_prefix: Optional[str] = None,
) -> None:
    """Configure the process-wide offload executor before it is created.

    The executor is built lazily on first use, so this must be called before any
    async request is dispatched. If the pool already exists a
    :class:`RuntimeError` is raised rather than tearing down a pool that may have
    work in flight; call :func:`shutdown_offload_executor` first to replace it.

    Args:
        max_workers: Maximum number of worker threads. ``None`` (the default)
            uses the :class:`~concurrent.futures.ThreadPoolExecutor` default of
            ``min(32, os.cpu_count() + 4)``.
        thread_name_prefix: Prefix for worker thread names, handy in profilers
            and stack dumps. ``None`` keeps the current prefix.

    Raises:
        RuntimeError: If the executor has already been created.
        ValueError: If ``max_workers`` is not a positive integer or ``None``.
    """
    _pool.configure(max_workers, thread_name_prefix)


def get_offload_executor() -> Executor:
    """Return the process-wide offload executor, creating it on first use."""
    return _pool.get()


async def run_offloaded(
    fn: Callable[..., T],
    *args: object,
    executor: Optional[Executor] = None,
    **kwargs: object,
) -> T:
    """Run blocking ``fn`` on the offload pool, propagating contextvars.

    ``loop.run_in_executor`` does not copy the caller's :mod:`contextvars`
    context (unlike :func:`asyncio.to_thread`), so tenant/correlation ids and
    logging filters set on the event loop would be invisible on the worker
    thread. This snapshots the context in the async task and runs ``fn`` inside
    it. Prefer it over ``loop.run_in_executor`` at offload sites that must
    observe the caller's context (transport sends, streaming reads, auth hooks,
    blocking file I/O).

    Args:
        fn: The blocking callable to run on the pool.
        *args: Positional arguments for ``fn``.
        executor: Optional executor; defaults to the process-wide offload pool
            from :func:`get_offload_executor`.
        **kwargs: Keyword arguments for ``fn``.

    Returns:
        Whatever ``fn`` returns.
    """
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    call = functools.partial(ctx.run, fn, *args, **kwargs)
    return await loop.run_in_executor(executor or get_offload_executor(), call)


def shutdown_offload_executor(wait: bool = True) -> None:
    """Shut down the shared offload executor and restore default settings.

    A no-op when the pool was never created. The next
    :func:`get_offload_executor` builds a fresh pool with default sizing, unless
    :func:`configure_offload_executor` is called again first.

    Args:
        wait: Whether to block until queued/running tasks finish.
    """
    _pool.shutdown(wait)
