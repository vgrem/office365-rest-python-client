"""Offline tests for the default ``requests``-backed transport.

Regression coverage for C1: a configured timeout (transport-level or
per-request) must actually reach ``requests`` instead of being silently dropped.
The bundled default bounds only the connect phase (10 s) while leaving reads
unbounded; ``NO_TIMEOUT`` disables timeouts entirely.
"""

from __future__ import annotations

import unittest
from typing import Any

import requests
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.transport.base import NO_TIMEOUT
from office365.runtime.transport.requests_transport import DEFAULT_TIMEOUT, RequestsTransport
from requests import Response


class _RecordingSession(requests.Session):
    """A ``Session`` that records the kwargs of every dispatched request."""

    def __init__(self) -> None:
        super().__init__()
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, url: str, **kwargs: Any) -> Response:  # type: ignore[override]
        self.calls.append((method, url, kwargs))
        response = Response()
        response.status_code = 200
        response.url = url
        response._content = b"{}"
        response._content_consumed = True
        return response


def _get(url: str = "https://contoso.sharepoint.com/_api/web") -> RequestOptions:
    return RequestOptions(url=url)


class TestRequestsTransportTimeout(unittest.TestCase):
    def test_configured_timeout_is_applied(self):
        session = _RecordingSession()
        transport = RequestsTransport(session=session, timeout=15)

        transport.execute(_get())

        self.assertEqual(session.calls[0][2]["timeout"], 15)

    def test_per_request_timeout_overrides_transport(self):
        session = _RecordingSession()
        transport = RequestsTransport(session=session, timeout=15)
        request = _get()
        request.timeout = 3

        transport.execute(request)

        self.assertEqual(session.calls[0][2]["timeout"], 3)

    def test_default_connect_timeout_is_applied(self):
        session = _RecordingSession()
        transport = RequestsTransport(session=session)

        transport.execute(_get())

        self.assertEqual(session.calls[0][2]["timeout"], DEFAULT_TIMEOUT)
        self.assertEqual(DEFAULT_TIMEOUT, (10.0, None))

    def test_no_timeout_sentinel_disables_timeout(self):
        session = _RecordingSession()
        transport = RequestsTransport(session=session, timeout=NO_TIMEOUT)

        transport.execute(_get())

        self.assertIsNone(transport.timeout)
        self.assertNotIn("timeout", session.calls[0][2])

    def test_tuple_timeout_is_forwarded(self):
        session = _RecordingSession()
        transport = RequestsTransport(session=session, timeout=(5, 30))

        transport.execute(_get())

        self.assertEqual(session.calls[0][2]["timeout"], (5, 30))

    def test_float_per_request_timeout_is_forwarded(self):
        session = _RecordingSession()
        transport = RequestsTransport(session=session)
        request = _get()
        request.timeout = 2.5

        transport.execute(request)

        self.assertEqual(session.calls[0][2]["timeout"], 2.5)

    def test_streaming_helper_applies_timeout(self):
        session = _RecordingSession()
        transport = RequestsTransport(session=session, timeout=9)
        request = _get()

        list(transport.stream(request))

        kwargs = session.calls[0][2]
        self.assertEqual(kwargs["timeout"], 9)
        self.assertTrue(kwargs["stream"])


if __name__ == "__main__":
    unittest.main()
