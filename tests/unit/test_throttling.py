"""Offline tests for throttling-header parsing and the rate-limit hooks."""

from __future__ import annotations

from office365.graph_client import GraphClient
from office365.runtime.http.throttling import ThrottleLimits, parse_throttling, rate_limit_hook, throttle_guard
from requests import Response


def _response(headers: dict) -> Response:
    resp = Response()
    resp.status_code = 200
    resp.headers = dict(headers)
    return resp


def test_parse_throttling_full():
    limits = parse_throttling(
        _response(
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
    assert parse_throttling(_response({})) is None


def test_parse_throttling_non_sharepoint_response():
    # Microsoft Graph responses carry no RateLimit-* headers
    assert parse_throttling(_response({"content-type": "application/json"})) is None


def test_parse_throttling_malformed_values():
    limits = parse_throttling(_response({"RateLimit-Remaining": "abc", "RateLimit-Reset": "30"}))
    assert limits == ThrottleLimits(remaining=None, reset=30)
    assert limits.remaining is None


def test_parse_throttling_health_score_only():
    # SharePoint sends X-SharePointHealthScore on every response, even without RateLimit-*
    limits = parse_throttling(_response({"X-SharePointHealthScore": "2"}))
    assert limits == ThrottleLimits(health_score=2)


def test_rate_limit_hook_fires_on_throttling_headers():
    seen = []
    hook = rate_limit_hook(seen.append)
    hook(_response({"RateLimit-Remaining": "5", "RateLimit-Reset": "30"}))
    assert len(seen) == 1
    assert seen[0].remaining == 5  # noqa: PLR2004


def test_rate_limit_hook_silent_without_headers():
    seen = []
    hook = rate_limit_hook(seen.append)
    hook(_response({}))
    assert seen == []


def test_throttle_guard_attaches_and_detaches():
    client = GraphClient()
    seen = []

    with throttle_guard(client, on_limits=seen.append):
        client.pending_request().afterExecute(_response({"RateLimit-Remaining": "7", "RateLimit-Reset": "10"}))
        assert len(seen) == 1
        assert seen[0].remaining == 7  # noqa: PLR2004

    # the hook is detached on exit — firing again does nothing
    client.pending_request().afterExecute(_response({"RateLimit-Remaining": "1"}))
    assert len(seen) == 1


def test_throttle_guard_without_callback_is_noop():
    client = GraphClient()
    with throttle_guard(client):
        client.pending_request().afterExecute(_response({"RateLimit-Remaining": "1"}))
