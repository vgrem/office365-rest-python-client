"""Offline tests for concurrent batch execution."""

from __future__ import annotations

import threading
import time
import unittest

from office365.runtime.queries.batch import BatchQuery
from office365.sharepoint.client_context import ClientContext


def _make_batches(ctx: ClientContext, count: int) -> list[BatchQuery]:
    return [BatchQuery(ctx) for _ in range(count)]


class _ParallelHarness(ClientContext):
    def __init__(self) -> None:
        super().__init__("https://contoso.sharepoint.com")
        self.executed: list[object] = []
        self.max_active = 0
        self._active = 0
        self._lock = threading.Lock()

    def _execute_batch(self, batch_qry):
        with self._lock:
            self._active += 1
            self.max_active = max(self.max_active, self._active)
        time.sleep(0.05)
        with self._lock:
            self._active -= 1
        self.executed.append(batch_qry)
        return [batch_qry]


class TestExecuteBatchesInParallel(unittest.TestCase):
    def test_batches_run_concurrently(self):
        ctx = _ParallelHarness()
        batches = _make_batches(ctx, 4)

        results = []
        ctx._execute_batches_in_parallel(batches, concurrency=4, success_callback=results.append)

        self.assertEqual(len(results), 4)
        self.assertEqual(len(ctx.executed), 4)
        self.assertGreater(ctx.max_active, 1)

    def test_failure_re_raised_without_success_callback(self):
        ctx = _ParallelHarness()

        def _boom(batch_qry):
            raise RuntimeError("boom")

        ctx._execute_batch = _boom  # type: ignore[method-assign]

        results = []
        batches = _make_batches(ctx, 2)
        with self.assertRaises(RuntimeError):
            ctx._execute_batches_in_parallel(batches, concurrency=2, success_callback=results.append)

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
