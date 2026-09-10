"""Merged unit tests (consolidated; see git history for originals)."""

from __future__ import annotations

import threading
import time
import unittest
from unittest import mock

import requests
from office365.graph_client import GraphClient
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.http.throttling import (
    RateLimiter,
    ThrottleLimits,
    parse_throttling,
    rate_limit_hook,
    throttle_guard,
)
from office365.runtime.operations import ProgressTracker
from office365.runtime.parallel import run_parallel
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.retry import backoff_delay, retry, retry_after_delay
from office365.runtime.types.event_handler import EventHandler
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.request import SharePointRequest
from office365.sharepoint.webs.context_web_information import ContextWebInformation
from requests import Response
from tests._scripted_transport import ScriptedTransport as _ScriptedTransport


def _make_error_response(status_code: int, headers: dict | None = None) -> Response:
    resp = Response()
    resp.status_code = status_code
    resp.url = "https://contoso.sharepoint.com/_api/web"
    resp.headers.update(headers or {})
    resp._content = b'{"error":{"code":"-1, System.Exception","message":"boom"}}'
    return resp


def _make_exception(status_code: int, headers: dict | None = None) -> ClientRequestException:
    return ClientRequestException.from_response(_make_error_response(status_code, headers))


def _make_context(outcomes: list[Exception | None]) -> tuple[ClientContext, mock.Mock]:
    """ClientContext whose execute_query replays the scripted outcomes.

    ``None`` signals a successful execution; an exception is raised as-is.
    Attempts are read from ``execute_query.call_count``.
    """
    ctx = ClientContext("https://contoso.sharepoint.com")
    execute_query = mock.Mock(side_effect=outcomes)
    ctx.execute_query = execute_query  # type: ignore[method-assign]
    return ctx, execute_query


class TestExecuteQueryRetry(unittest.TestCase):
    def test_permanent_error_raises_immediately(self):
        ctx, execute_query = _make_context([_make_exception(400)])

        with mock.patch("office365.runtime.retry.sleep") as sleep_mock:
            with self.assertRaises(ClientRequestException):
                ctx.execute_query_retry(max_retry=5, timeout_secs=5)

        self.assertEqual(execute_query.call_count, 1)
        sleep_mock.assert_not_called()

    def test_transient_then_success(self):
        ctx, execute_query = _make_context([_make_exception(429), None])

        with mock.patch("office365.runtime.retry.sleep") as sleep_mock:
            ctx.execute_query_retry(max_retry=5, timeout_secs=5, jitter=False)

        self.assertEqual(execute_query.call_count, 2)
        sleep_mock.assert_called_once_with(5)

    def test_retries_exhausted_raises_last_error(self):
        ctx, execute_query = _make_context([_make_exception(503), _make_exception(503), _make_exception(503)])

        with self.assertRaises(ClientRequestException) as cm:
            ctx.execute_query_retry(max_retry=2, timeout_secs=1)

        self.assertEqual(execute_query.call_count, 2)
        assert cm.exception.response is not None
        self.assertEqual(cm.exception.response.status_code, 503)

    def test_non_http_error_is_retried(self):
        ctx, execute_query = _make_context([requests.ConnectionError("boom"), None])

        ctx.execute_query_retry(
            max_retry=5,
            timeout_secs=1,
            exceptions=(ClientRequestException, requests.RequestException),
        )

        self.assertEqual(execute_query.call_count, 2)

    def test_incremental_retry_does_not_retry_permanent_error(self):
        ctx, execute_query = _make_context([_make_exception(400)])

        with self.assertRaises(ClientRequestException):
            ctx.execute_query_with_incremental_retry(max_retry=5)

        self.assertEqual(execute_query.call_count, 1)

    def test_incremental_retry_applies_retry_after(self):
        ctx, execute_query = _make_context([_make_exception(429, {"Retry-After": "10"}), None])

        with mock.patch("office365.runtime.retry.sleep") as sleep_mock:
            ctx.execute_query_with_incremental_retry(max_retry=5)

        self.assertEqual(execute_query.call_count, 2)
        sleep_mock.assert_called_once_with(10)

    def test_incremental_retry_falls_back_to_exponential_backoff(self):
        ctx, execute_query = _make_context([_make_exception(503), None])

        with mock.patch("office365.runtime.retry.sleep") as sleep_mock:
            ctx.execute_query_with_incremental_retry(max_retry=5, jitter=False)

        self.assertEqual(execute_query.call_count, 2)
        sleep_mock.assert_called_once_with(5)


class TestRetryFunction(unittest.TestCase):
    def test_exponential_backoff_capped_by_max_delay(self):
        func = mock.Mock(side_effect=[_make_exception(503), _make_exception(503), "ok"])

        with mock.patch("office365.runtime.retry.sleep") as sleep_mock:
            retry(func, max_retry=5, timeout_secs=2, max_delay=3, jitter=False)

        sleep_mock.assert_has_calls([mock.call(2), mock.call(3)])

    def test_non_transient_error_raises_immediately(self):
        func = mock.Mock(side_effect=_make_exception(400))

        with mock.patch("office365.runtime.retry.sleep") as sleep_mock:
            with self.assertRaises(ClientRequestException):
                retry(func, max_retry=5, timeout_secs=2)

        self.assertEqual(func.call_count, 1)
        sleep_mock.assert_not_called()

    def test_on_failure_overrides_timeout(self):
        func = mock.Mock(side_effect=[_make_exception(503), "ok"])

        with mock.patch("office365.runtime.retry.sleep") as sleep_mock:
            retry(func, max_retry=5, timeout_secs=2, on_failure=lambda _attempt, _ex: 10)

        sleep_mock.assert_called_once_with(10)

    def test_retries_exhausted_raises_last_error(self):
        func = mock.Mock(side_effect=_make_exception(503))

        with self.assertRaises(ClientRequestException) as cm:
            retry(func, max_retry=2, timeout_secs=1)

        self.assertEqual(func.call_count, 2)
        assert cm.exception.response is not None
        self.assertEqual(cm.exception.response.status_code, 503)


class TestRetryAfterDelay(unittest.TestCase):
    def test_returns_retry_after_value(self):
        ex = _make_exception(429, {"Retry-After": "10"})
        self.assertEqual(retry_after_delay(ex), 10)

    def test_returns_none_for_non_throttling_status(self):
        ex = _make_exception(400)
        self.assertIsNone(retry_after_delay(ex))


class TestBackoffDelay(unittest.TestCase):
    def test_exponential_growth(self):
        self.assertEqual(backoff_delay(1, base=5, jitter=False), 5)
        self.assertEqual(backoff_delay(2, base=5, jitter=False), 10)  # noqa: PLR2004
        self.assertEqual(backoff_delay(3, base=5, jitter=False), 20)  # noqa: PLR2004

    def test_capped_by_max_delay(self):
        self.assertEqual(backoff_delay(3, base=5, max_delay=12, jitter=False), 12)  # noqa: PLR2004

    def test_jitter_within_bounds(self):
        for attempt in (1, 2, 3):  # noqa: PLR2004
            nominal = backoff_delay(attempt, base=5, jitter=False)
            for _ in range(50):  # noqa: PLR2004
                delay = backoff_delay(attempt, base=5)
                self.assertGreaterEqual(delay, 0)
                self.assertLessEqual(delay, nominal)


class TestContextStateAfterRetryFailure(unittest.TestCase):
    """Issue #938 — execute_query_retry must not leave the context dirty."""

    def test_exhausted_retries_leave_queue_clean(self):
        from office365.runtime.queries.client_query import ClientQuery

        ctx = ClientContext("https://contoso.sharepoint.com")
        qry = ClientQuery(ctx)
        ctx.add_query(qry)
        attempts = {"n": 0}

        def _execute_query():
            attempts["n"] += 1
            if ctx._queries:
                ctx._current_query = ctx._queries.popleft()
            raise _make_exception(503)

        ctx.execute_query = _execute_query  # type: ignore[method-assign]

        with mock.patch("office365.runtime.retry.sleep"):
            with self.assertRaises(ClientRequestException):
                ctx.execute_query_retry(max_retry=3, timeout_secs=5, jitter=False)

        self.assertEqual(attempts["n"], 3)  # noqa: PLR2004
        # no stale query left queued and no cursor retained
        self.assertEqual(len(ctx._queries), 0)
        self.assertIsNone(ctx.current_query)

    def test_permanent_error_leaves_queue_clean(self):
        from office365.runtime.queries.client_query import ClientQuery

        ctx = ClientContext("https://contoso.sharepoint.com")
        qry = ClientQuery(ctx)
        ctx.add_query(qry)

        def _execute_query():
            if ctx._queries:
                ctx._current_query = ctx._queries.popleft()
            raise _make_exception(400)

        ctx.execute_query = _execute_query  # type: ignore[method-assign]

        with mock.patch("office365.runtime.retry.sleep"):
            with self.assertRaises(ClientRequestException):
                ctx.execute_query_retry(max_retry=3, timeout_secs=5, jitter=False)

        self.assertEqual(len(ctx._queries), 0)
        self.assertIsNone(ctx.current_query)


def throttling__response(headers: dict) -> Response:
    resp = Response()
    resp.status_code = 200
    resp.headers = dict(headers)
    return resp


def test_parse_throttling_full():
    limits = parse_throttling(
        throttling__response(
            {
                "RateLimit-Limit": "600",
                "RateLimit-Remaining": "540",
                "RateLimit-Reset": "23",
                "Retry-After": "5",
                "X-SharePointHealthScore": "90",
            }
        )
    )
    assert limits == ThrottleLimits(limit=600, remaining=540, reset=23, retry_after=5, health_score=90)


def test_parse_throttling_absent_headers():
    assert parse_throttling(throttling__response({})) is None


def test_parse_throttling_non_sharepoint_response():
    # Microsoft Graph responses carry no RateLimit-* headers
    assert parse_throttling(throttling__response({"content-type": "application/json"})) is None


def test_parse_throttling_malformed_values():
    limits = parse_throttling(throttling__response({"RateLimit-Remaining": "abc", "RateLimit-Reset": "30"}))
    assert limits == ThrottleLimits(remaining=None, reset=30)
    assert limits.remaining is None


def test_parse_throttling_health_score_only():
    # SharePoint sends X-SharePointHealthScore on every response, even without RateLimit-*
    limits = parse_throttling(throttling__response({"X-SharePointHealthScore": "2"}))
    assert limits == ThrottleLimits(health_score=2)


def test_rate_limit_hook_fires_on_throttling_headers():
    seen = []
    hook = rate_limit_hook(seen.append)
    hook(throttling__response({"RateLimit-Remaining": "5", "RateLimit-Reset": "30"}))
    assert len(seen) == 1
    assert seen[0].remaining == 5  # noqa: PLR2004


def test_rate_limit_hook_silent_without_headers():
    seen = []
    hook = rate_limit_hook(seen.append)
    hook(throttling__response({}))
    assert seen == []


def test_throttle_guard_attaches_and_detaches():
    client = GraphClient()
    seen = []

    with throttle_guard(client, on_limits=seen.append):
        client.pending_request().afterExecute(
            throttling__response({"RateLimit-Remaining": "7", "RateLimit-Reset": "10"})
        )
        assert len(seen) == 1
        assert seen[0].remaining == 7  # noqa: PLR2004

    # the hook is detached on exit — firing again does nothing
    client.pending_request().afterExecute(throttling__response({"RateLimit-Remaining": "1"}))
    assert len(seen) == 1


def ratelimiter__response(retry_after: str | None = None, health_score: str | None = None) -> Response:
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
    def test_retry_after_gates_the_group(self):
        limiter = RateLimiter()
        limiter.observe(ratelimiter__response(retry_after="1"))

        elapsed = _elapsed(limiter.acquire)
        self.assertGreaterEqual(elapsed, 0.9)
        self.assertLess(elapsed, 2.0)

    def test_health_score_above_threshold_paces(self):
        limiter = RateLimiter(health_threshold=80)
        limiter.observe(ratelimiter__response(health_score="90"))
        self.assertGreaterEqual(_elapsed(limiter.acquire), 0.4)

    def test_acquire_is_thread_safe_and_shares_the_gate(self):
        limiter = RateLimiter()
        observed = [0.0]

        def _worker():
            observed[0] = time.monotonic()
            limiter.acquire()

        limiter.observe(ratelimiter__response(retry_after="1"))
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


def test_report_emits_progress_with_total():
    seen = []
    tracker = ProgressTracker(seen.append, total=10, stage="uploading")

    tracker.report(3)
    tracker.report(5)

    assert [p.done for p in seen] == [3, 5]
    assert all(p.total == 10 for p in seen)  # noqa: PLR2004
    assert all(p.stage == "uploading" for p in seen)


def test_advance_and_late_total():
    seen = []
    tracker = ProgressTracker(seen.append, stage="migrating")

    tracker.advance()
    tracker.advance(2)
    tracker.set_total(10)
    tracker.report(5)

    assert [p.done for p in seen] == [1, 3, 5]
    assert seen[-1].total == 10  # noqa: PLR2004
    assert seen[-1].percent == 50.0  # noqa: PLR2004


def test_report_is_monotonic():
    seen = []
    tracker = ProgressTracker(seen.append, total=100, stage="loading")

    tracker.report(40)
    tracker.report(30)  # out-of-order completion must not go backwards

    assert [p.done for p in seen] == [40, 40]


def test_thread_safe_advances_sum_to_total():
    seen = []
    tracker = ProgressTracker(seen.append, total=1000, stage="parallel")
    threads = [threading.Thread(target=lambda: [tracker.advance() for _ in range(100)]) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert tracker.done == 1000  # noqa: PLR2004
    assert len(seen) == 1000  # noqa: PLR2004


def _run_concurrently(target, count: int = 2) -> None:
    barrier = threading.Barrier(count)

    def _wrapped():
        barrier.wait()
        target()

    threads = [threading.Thread(target=_wrapped) for _ in range(count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


class TestThreadSafety(unittest.TestCase):
    def test_with_access_token_single_flight(self):
        auth_ctx = AuthenticationContext("https://contoso.sharepoint.com")
        calls: list[int] = []

        def token_func():
            calls.append(1)
            time.sleep(0.1)
            return {"accessToken": "token", "tokenType": "Bearer", "expiresIn": 3600}

        auth_ctx.with_access_token(token_func)

        def _authenticate():
            auth_ctx.authenticate_request(RequestOptions("https://contoso.sharepoint.com"))

        _run_concurrently(_authenticate)

        self.assertEqual(len(calls), 1)

    def test_ensure_form_digest_single_flight(self):
        request = SharePointRequest("https://contoso.sharepoint.com")
        context_info = ContextWebInformation(
            FormDigestValue="digest",
            FormDigestTimeoutSeconds=1800,
            _valid_from=time.time(),
        )
        fetch = mock.Mock(return_value=context_info)
        request._get_context_web_information = fetch  # type: ignore[method-assign]

        requests_with_header = []

        def _ensure():
            req = RequestOptions("https://contoso.sharepoint.com")
            request.ensure_form_digest(req)
            requests_with_header.append(req)

        _run_concurrently(_ensure)

        fetch.assert_called_once()
        self.assertTrue(all(req.headers.get("X-RequestDigest") == "digest" for req in requests_with_header))

    def test_split_batches_preserves_order_and_drains_queue(self):
        ctx = ClientContext("https://contoso.sharepoint.com")
        for _ in range(250):
            ctx.add_query(ClientQuery(ctx))

        batches = ctx._split_batches(100)

        self.assertEqual([len(batch.queries) for batch in batches], [100, 100, 50])
        self.assertFalse(ctx.has_pending_request)
        self.assertIsNone(ctx._current_query)

    def test_clone_shares_auth_and_transport(self):
        ctx = ClientContext("https://contoso.sharepoint.com")
        ctx.add_query(ClientQuery(ctx))
        source_request = ctx.pending_request()

        clone = ctx.clone("https://contoso-admin.sharepoint.com")

        clone_request = clone.pending_request()
        self.assertIs(clone_request.authentication_context, source_request.authentication_context)
        self.assertIs(clone_request.transport, source_request.transport)
        self.assertFalse(clone.has_pending_request)
        self.assertTrue(ctx.has_pending_request)

    def test_clone_keeps_pending_queries(self):
        ctx = ClientContext("https://contoso.sharepoint.com")
        for _ in range(3):
            ctx.add_query(ClientQuery(ctx))

        clone = ctx.clone("https://contoso-admin.sharepoint.com", clear_queries=False)

        self.assertEqual(len(clone._queries), 3)
        self.assertTrue(clone.has_pending_request)
