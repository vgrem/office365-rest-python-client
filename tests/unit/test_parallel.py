"""Offline tests for the generic run_parallel primitive."""

from __future__ import annotations

import threading
import time
import unittest

from office365.runtime.parallel import run_parallel
from office365.runtime.types.event_handler import EventHandler


class _Pending:
    def __init__(self) -> None:
        self.beforeExecute = EventHandler()
        self.afterExecute = EventHandler()
        self.onError = EventHandler()


class _FakeContext:
    def __init__(self) -> None:
        self.pending = _Pending()

    def pending_request(self):
        return self.pending


class TestRunParallel(unittest.TestCase):
    def test_ordered_results(self):
        results = run_parallel(lambda _ctx, task: task * 2, [1, 2, 3], concurrency=3)
        self.assertEqual(results, [2, 4, 6])  # noqa: PLR2004

    def test_empty_is_noop(self):
        self.assertEqual(run_parallel(lambda _ctx, task: task, []), [])

    def test_context_factory_once_per_thread_and_limiter_bound(self):
        contexts = []
        lock = threading.Lock()

        def factory():
            ctx = _FakeContext()
            with lock:
                contexts.append(ctx)
            return ctx

        def _worker(ctx, task):
            time.sleep(0.02)  # keep both pool threads busy so both create a context
            return (id(ctx), task)

        results = run_parallel(
            _worker,
            [1, 2, 3, 4],  # noqa: PLR2004
            concurrency=2,  # noqa: PLR2004
            context_factory=factory,
        )

        self.assertEqual(len(contexts), 2)  # noqa: PLR2004 — one context per worker thread
        self.assertEqual(len({r[0] for r in results}), 2)  # noqa: PLR2004
        for ctx in contexts:
            self.assertEqual(len(ctx.pending.beforeExecute), 1)
            self.assertEqual(len(ctx.pending.afterExecute), 1)
            self.assertEqual(len(ctx.pending.onError), 1)

    def test_on_error_returns_fallback(self):
        def worker(_ctx, task):
            if task == 2:  # noqa: PLR2004
                raise ValueError("boom")
            return task

        results = run_parallel(worker, [1, 2, 3], on_error=lambda _t, _e: -1)
        self.assertEqual(results, [1, -1, 3])

    def test_without_on_error_raises(self):
        def worker(_ctx, task):
            raise ValueError("boom")

        with self.assertRaises(ValueError):
            run_parallel(worker, [1], concurrency=1)

    def test_progress_fires_per_task(self):
        seen = []
        run_parallel(lambda _ctx, task: task, [1, 2, 3], progress=lambda p: seen.append(p.done))
        self.assertEqual(sorted(seen), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
