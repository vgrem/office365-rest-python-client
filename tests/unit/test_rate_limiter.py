"""Offline tests for the shared, concurrency-aware RateLimiter."""

from __future__ import annotations

import threading
import time
import unittest

from office365.runtime.http.throttling import RateLimiter
from office365.sharepoint.client_context import ClientContext
from requests import Response
from tests._scripted_transport import ScriptedTransport as _ScriptedTransport


def _response(retry_after: str | None = None, health_score: str | None = None) -> Response:
    resp = Response()
    resp.status_code = 429 if retry_after else 200
    resp.headers["Content-Type"] = "application/json"
    if retry_after:
        resp.headers["Retry-After"] = retry_after
    if health_score:
        resp.headers["X-SharePointHealthScore"] = health_score
    resp._content = b"{}"
    return resp


def _elapsed(fn) -> float:
    start = time.monotonic()
    fn()
    return time.monotonic() - start


class TestRateLimiter(unittest.TestCase):
    def test_acquire_is_instant_without_gate(self):
        limiter = RateLimiter()
        self.assertLess(_elapsed(limiter.acquire), 0.2)

    def test_retry_after_gates_the_group(self):
        limiter = RateLimiter()
        limiter.observe(_response(retry_after="1"))

        elapsed = _elapsed(limiter.acquire)
        self.assertGreaterEqual(elapsed, 0.9)
        self.assertLess(elapsed, 2.0)

    def test_health_score_above_threshold_paces(self):
        limiter = RateLimiter(health_threshold=80)
        limiter.observe(_response(health_score="90"))
        self.assertGreaterEqual(_elapsed(limiter.acquire), 0.4)

    def test_health_score_below_threshold_is_free(self):
        limiter = RateLimiter(health_threshold=80)
        limiter.observe(_response(health_score="40"))
        self.assertLess(_elapsed(limiter.acquire), 0.2)

    def test_acquire_is_thread_safe_and_shares_the_gate(self):
        limiter = RateLimiter()
        observed = [0.0]

        def _worker():
            observed[0] = time.monotonic()
            limiter.acquire()

        limiter.observe(_response(retry_after="1"))
        thread = threading.Thread(target=_worker)
        start = time.monotonic()
        thread.start()
        thread.join()
        self.assertGreaterEqual(time.monotonic() - start, 0.9)

    def test_bind_attaches_hooks_and_reports_to_limiter(self):
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
        ctx.pending_request().beforeExecute.clear()
        ctx.pending_request().afterExecute.clear()
        limiter = RateLimiter()
        limiter.bind(ctx)

        self.assertEqual(len(ctx.pending_request().beforeExecute), 1)
        self.assertEqual(len(ctx.pending_request().afterExecute), 1)

        ctx.pending_request().transport = _ScriptedTransport([{"status": 429, "retry_after": 2, "body": {}}])
        ctx.load(ctx.web).execute_query()

        # the 429 response observed by the hook must gate the group
        self.assertGreaterEqual(_elapsed(limiter.acquire), 1.8)


if __name__ == "__main__":
    unittest.main()
