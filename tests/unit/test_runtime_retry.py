"""Retry, throttling and pacing: what is transient, how long to wait, what the limiter learns."""

from __future__ import annotations

import threading
import time
import unittest
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from unittest import mock

import pytest
import requests
from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.http.throttling import (
    PaceState,
    RateLimiter,
    ThrottleLimits,
    pace,
    parse_throttling,
    throttle_guard,
)
from office365.runtime.operations import ProgressTracker
from office365.runtime.retry import (
    backoff_delay,
    is_transient_error,
    response_retry_after,
    retry,
    should_reset_connections,
)
from requests import Response


def _make_error_response(status_code: int, headers: dict | None = None) -> Response:
    resp = Response()
    resp.status_code = status_code
    resp.url = "https://contoso.sharepoint.com/_api/web"
    resp.headers.update(headers or {})
    resp._content = b'{"error":{"code":"-1, System.Exception","message":"boom"}}'
    return resp


def _response_with_retry_after(value: str) -> Response:
    resp = Response()
    resp.status_code = 503
    resp.headers["Retry-After"] = value
    return resp


def _make_exception(status_code: int, headers: dict | None = None) -> ClientRequestException:
    return ClientRequestException.from_response(_make_error_response(status_code, headers))


class TestRetryFunction(unittest.TestCase):
    def test_invalid_url_is_not_retried(self):
        func = mock.Mock(side_effect=requests.exceptions.InvalidURL("nope"))

        with mock.patch("office365.runtime.retry.sleep") as sleep_mock:
            with self.assertRaises(requests.exceptions.InvalidURL):
                retry(func, max_retry=5, timeout_secs=1)

        self.assertEqual(func.call_count, 1)
        sleep_mock.assert_not_called()

    def test_max_delay_bounds_the_wait_the_server_asks_for(self):
        """A caller who names a ceiling keeps it, whatever ``Retry-After`` says."""
        func = mock.Mock(side_effect=[_make_exception(429, {"Retry-After": "600"}), None])

        with mock.patch("office365.runtime.retry.sleep") as sleep_mock:
            retry(func, max_retry=5, max_delay=30)

        sleep_mock.assert_called_once_with(30)


class TestTransportErrorClassification(unittest.TestCase):
    """A transport failure is retried only if the connection might heal."""

    def test_only_connection_failures_are_transient(self):
        transient = [
            requests.ConnectionError("boom"),
            requests.Timeout("slow"),
            requests.exceptions.ChunkedEncodingError("cut"),
        ]
        permanent = [
            requests.exceptions.SSLError("bad cert"),
            requests.exceptions.InvalidURL("nope"),
        ]
        self.assertTrue(all(is_transient_error(err) for err in transient))
        self.assertFalse(any(is_transient_error(err) for err in permanent))

    def test_a_reset_is_for_a_broken_connection_not_a_refusal(self):
        self.assertTrue(should_reset_connections(_make_exception(503)))
        self.assertTrue(should_reset_connections(requests.ConnectionError("boom")))
        self.assertFalse(should_reset_connections(_make_exception(429)))
        self.assertFalse(should_reset_connections(_make_exception(400)))
        self.assertFalse(should_reset_connections(requests.exceptions.SSLError("bad cert")))


class TestRetryAfterDelay(unittest.TestCase):
    def test_parses_http_date(self):
        future = datetime.now(timezone.utc) + timedelta(seconds=30)
        value = format_datetime(future, usegmt=True)
        self.assertGreaterEqual(response_retry_after(_response_with_retry_after(value)), 28)
        self.assertLessEqual(response_retry_after(_response_with_retry_after(value)), 30)


class TestBackoffDelay(unittest.TestCase):
    def test_exponential_growth(self):
        self.assertEqual(backoff_delay(1, base=5, jitter=False), 5)
        self.assertEqual(backoff_delay(2, base=5, jitter=False), 10)  # noqa: PLR2004
        self.assertEqual(backoff_delay(3, base=5, jitter=False), 20)  # noqa: PLR2004

    def test_jitter_within_bounds(self):
        for attempt in (1, 2, 3):  # noqa: PLR2004
            nominal = backoff_delay(attempt, base=5, jitter=False)
            for _ in range(50):  # noqa: PLR2004
                delay = backoff_delay(attempt, base=5)
                self.assertGreaterEqual(delay, 0)
                self.assertLessEqual(delay, nominal)


def throttling__response(headers: dict) -> Response:
    resp = Response()
    resp.status_code = 200
    resp.headers.update(headers)
    return resp


def test_parse_throttling_malformed_values():
    limits = parse_throttling(throttling__response({"RateLimit-Remaining": "abc", "RateLimit-Reset": "30"}))
    assert limits == ThrottleLimits(remaining=None, reset=30, status=200)
    assert limits is not None
    assert limits.remaining is None


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


def ratelimiter__response(
    retry_after: str | None = None,
    health_score: str | None = None,
    limit_percentage: str | None = None,
    resource_unit: str | None = None,
    scope: str | None = None,
    reason: str | None = None,
) -> Response:
    resp = Response()
    resp.status_code = 429 if retry_after else 200
    resp.headers["Content-Type"] = "application/json"
    if retry_after:
        resp.headers["Retry-After"] = retry_after
    if health_score:
        resp.headers["X-SharePointHealthScore"] = health_score
    if limit_percentage:
        resp.headers["x-ms-throttle-limit-percentage"] = limit_percentage
    if resource_unit:
        resp.headers["x-ms-resource-unit"] = resource_unit
    if scope:
        resp.headers["x-ms-throttle-scope"] = scope
    if reason:
        resp.headers["x-ms-throttle-information"] = reason
    resp._content = b"{}"
    return resp


def _elapsed(fn) -> float:
    start = time.monotonic()
    fn()
    return time.monotonic() - start


class _FakeClock:
    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:
        return self.t


class TestRateLimiter(unittest.TestCase):
    def test_retry_after_gates_the_group(self):
        limiter = RateLimiter()
        limiter.observe(ratelimiter__response(retry_after="1"))

        elapsed = _elapsed(limiter.acquire)
        self.assertGreaterEqual(elapsed, 0.9)
        self.assertLess(elapsed, 2.0)

    def test_scope_signal_gates_the_group_by_default(self):
        limiter = RateLimiter(clock=_FakeClock(), sleep=lambda _delay: None)

        limiter.observe(ratelimiter__response(retry_after="5", scope="Mail.ReadWrite", reason="CPULimitExceeded"))

        self.assertGreaterEqual(limiter.snapshot().next_available_at, 5.0)
        self.assertEqual(limiter.last_scope, "Mail.ReadWrite")
        self.assertEqual(limiter.last_reason, "CPULimitExceeded")

    def test_per_scope_isolates_the_throttled_scope(self):
        clock = _FakeClock()
        slept: list[float] = []

        def _sleep(delay: float) -> None:
            slept.append(delay)
            clock.t += delay

        limiter = RateLimiter(per_scope=True, clock=clock, sleep=_sleep)
        limiter.observe(ratelimiter__response(retry_after="5", scope="Mail.ReadWrite"))

        # global gate is untouched and an unrelated scope is not gated
        self.assertEqual(limiter.snapshot().next_available_at, 0.0)
        limiter.acquire("Files.Read")
        self.assertEqual(slept, [])

        self.assertEqual(limiter.snapshot("Mail.ReadWrite").next_available_at, 5.0)
        limiter.acquire("Mail.ReadWrite")
        self.assertGreaterEqual(sum(slept), 5.0)

        limiter.reset()
        self.assertEqual(limiter.snapshot("Mail.ReadWrite").next_available_at, 0.0)
        self.assertIsNone(limiter.last_scope)


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


def test_parse_throttling_graph_headers():
    limits = parse_throttling(
        throttling__response(
            {
                "Retry-After": "10",
                "x-ms-throttle-limit-percentage": "1.2",
                "x-ms-resource-unit": "3",
                "x-ms-throttle-scope": "Tenant_Application/ReadWrite/app/tenant",
                "x-ms-throttle-information": "WriteLimitExceeded",
            }
        )
    )
    assert limits is not None
    assert limits.retry_after == 10  # noqa: PLR2004
    assert limits.limit_percentage == 1.2  # noqa: PLR2004
    assert limits.resource_unit == 3  # noqa: PLR2004
    assert limits.scope == "Tenant_Application/ReadWrite/app/tenant"
    assert limits.reason == "WriteLimitExceeded"


def test_pace_reacts_to_graph_limit_percentage():
    now = 1000.0
    assert pace(PaceState(), ThrottleLimits(limit_percentage=1.2), now=now).next_available_at > now
    # below the threshold -> no pacing
    assert pace(PaceState(), ThrottleLimits(limit_percentage=0.5), now=now) == PaceState()


def test_with_throttle_priority_sets_request_header():
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.with_throttle_priority("high")
    request = RequestOptions(url="https://graph.microsoft.com/v1.0/me")

    client.pending_request().beforeExecute(request)

    assert request.headers.get("x-ms-throttle-priority") == "high"


def test_with_throttle_priority_rejects_bad_value():
    with pytest.raises(ValueError, match="priority"):
        GraphClient().with_throttle_priority("urgent")
