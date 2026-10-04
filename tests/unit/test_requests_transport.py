"""Offline tests for the default ``requests``-backed transport.

Regression coverage for C1: a configured timeout (transport-level or
per-request) must actually reach ``requests`` instead of being silently dropped.
The bundled default bounds only the connect phase (10 s) while leaving reads
unbounded; ``NO_TIMEOUT`` disables timeouts entirely.
"""

from __future__ import annotations

import unittest
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, TypeVar
from unittest import mock

import requests
from office365.graph_client import GraphClient
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.transport.base import NO_TIMEOUT
from office365.runtime.transport.requests_transport import (
    DEFAULT_POOL_CONNECTIONS,
    DEFAULT_POOL_MAXSIZE,
    DEFAULT_TIMEOUT,
    RequestsTransport,
)
from requests import Response
from requests.adapters import HTTPAdapter

_T = TypeVar("_T")


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


class _ClosingRecordingSession(_RecordingSession):
    """A recording session that counts how often it was closed."""

    def __init__(self) -> None:
        super().__init__()
        self.close_calls = 0

    def close(self) -> None:
        self.close_calls += 1
        super().close()


def _get(url: str = "https://contoso.sharepoint.com/_api/web") -> RequestOptions:
    return RequestOptions(url=url)


def _run_on_worker(pool: ThreadPoolExecutor, fn: Callable[..., _T], *args: Any) -> _T:
    """Run ``fn`` on an existing single-worker pool so the thread is reused."""
    return pool.submit(fn, *args).result()


class TestRequestsTransportThreadLocalSessions(unittest.TestCase):
    """The default transport must not share one ``Session`` across threads."""

    def test_default_transport_creates_one_session_per_thread(self):
        with mock.patch("office365.runtime.transport.requests_transport.Session", _RecordingSession):
            transport = RequestsTransport(timeout=NO_TIMEOUT)

            transport.execute(_get())
            transport.execute(_get())  # reused on the same thread
            self.assertEqual(len(transport._sessions), 1)

            with ThreadPoolExecutor(max_workers=1) as pool:
                _run_on_worker(pool, transport.execute, _get())
                _run_on_worker(pool, transport.execute, _get())  # reused on that worker

            self.assertEqual(len(transport._sessions), 2)
            self.assertIsNot(transport._sessions[0], transport._sessions[1])
            self.assertEqual(len(transport._sessions[0].calls), 2)
            self.assertEqual(len(transport._sessions[1].calls), 2)

    def test_explicit_session_is_shared_across_threads(self):
        session = _RecordingSession()
        transport = RequestsTransport(session=session, timeout=NO_TIMEOUT)

        transport.execute(_get())
        with ThreadPoolExecutor(max_workers=1) as pool:
            _run_on_worker(pool, transport.execute, _get())

        self.assertEqual(transport._sessions, [session])
        self.assertEqual(len(session.calls), 2)
        self.assertIs(transport.auth, session.auth)

    def test_auth_is_none_before_a_thread_session_exists(self):
        with mock.patch("office365.runtime.transport.requests_transport.Session", _RecordingSession):
            self.assertIsNone(RequestsTransport().auth)

    def test_reset_connections_only_closes_the_calling_thread_session(self):
        with mock.patch("office365.runtime.transport.requests_transport.Session", _ClosingRecordingSession):
            transport = RequestsTransport(timeout=NO_TIMEOUT)
            transport.execute(_get())
            with ThreadPoolExecutor(max_workers=1) as pool:
                _run_on_worker(pool, transport.execute, _get())
                main_session, worker_session = transport._sessions

                transport.reset_connections()
                self.assertEqual(main_session.close_calls, 1)
                self.assertEqual(worker_session.close_calls, 0)

                _run_on_worker(pool, transport.reset_connections)
                self.assertEqual(worker_session.close_calls, 1)

    def test_close_closes_every_thread_session(self):
        with mock.patch("office365.runtime.transport.requests_transport.Session", _ClosingRecordingSession):
            transport = RequestsTransport(timeout=NO_TIMEOUT)
            transport.execute(_get())
            with ThreadPoolExecutor(max_workers=1) as pool:
                _run_on_worker(pool, transport.execute, _get())

            transport.close()

            self.assertTrue(all(s.close_calls == 1 for s in transport._sessions))


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


class TestRequestsTransportConnectionPool(unittest.TestCase):
    """Connection-pool sizing of the lazily-created per-thread sessions."""

    def test_defaults_match_requests(self):
        transport = RequestsTransport()

        self.assertEqual(transport.pool_connections, DEFAULT_POOL_CONNECTIONS)
        self.assertEqual(transport.pool_maxsize, DEFAULT_POOL_MAXSIZE)
        self.assertFalse(transport.pool_block)

    def test_configured_pool_applied_to_created_session(self):
        transport = RequestsTransport(pool_connections=5, pool_maxsize=25, pool_block=True)

        adapter = transport._current_session().get_adapter("https://contoso.sharepoint.com")

        self.assertIsInstance(adapter, HTTPAdapter)
        self.assertEqual(adapter._pool_connections, 5)
        self.assertEqual(adapter._pool_maxsize, 25)
        self.assertTrue(adapter._pool_block)

    def test_pool_applied_to_every_thread_session(self):
        transport = RequestsTransport(pool_connections=3, pool_maxsize=7)

        with mock.patch("office365.runtime.transport.requests_transport.Session", _RecordingSession):
            transport.execute(_get())
            with ThreadPoolExecutor(max_workers=1) as pool:
                _run_on_worker(pool, transport.execute, _get())

        for session in transport._sessions:
            adapter = session.get_adapter("https://contoso.sharepoint.com")
            self.assertEqual(adapter._pool_connections, 3)
            self.assertEqual(adapter._pool_maxsize, 7)

    def test_explicit_session_keeps_its_own_adapters(self):
        session = requests.Session()
        original = session.get_adapter("https://contoso.sharepoint.com")

        transport = RequestsTransport(session=session, pool_maxsize=99)

        self.assertEqual(transport._sessions, [session])
        self.assertIs(session.get_adapter("https://contoso.sharepoint.com"), original)
        self.assertEqual(original._pool_maxsize, DEFAULT_POOL_MAXSIZE)

    def test_invalid_pool_sizes_are_rejected(self):
        with self.assertRaises(ValueError):
            RequestsTransport(pool_connections=0)
        with self.assertRaises(ValueError):
            RequestsTransport(pool_maxsize=0)

    def test_with_transport_forwards_pool_sizing(self):
        ctx = GraphClient().with_transport(pool_connections=4, pool_maxsize=42, pool_block=True)

        transport = ctx.pending_request().transport

        self.assertEqual(transport.pool_connections, 4)
        self.assertEqual(transport.pool_maxsize, 42)
        self.assertTrue(transport.pool_block)


class TestRequestsTransportTlsAndProxy(unittest.TestCase):
    """Transport-level verify/proxies must actually reach ``requests``.

    Regression coverage: ``RequestOptions.verify`` used to default to ``True``,
    so ``with_transport(verify=False)`` was silently overridden and a custom CA
    bundle on a supplied session was clobbered; ``with_transport(proxies=...)``
    never reached the wire at all.
    """

    def test_default_verify_defers_to_the_session(self):
        self.assertIsNone(RequestsTransport().verify)

    def test_transport_verify_is_applied(self):
        session = _RecordingSession()
        transport = RequestsTransport(session=session, verify=False, timeout=NO_TIMEOUT)

        transport.execute(_get())

        self.assertFalse(session.calls[0][2]["verify"])

    def test_transport_proxies_are_applied(self):
        session = _RecordingSession()
        transport = RequestsTransport(session=session, proxies={"https": "http://proxy:8080"}, timeout=NO_TIMEOUT)

        transport.execute(_get())

        self.assertEqual(session.calls[0][2]["proxies"], {"https": "http://proxy:8080"})

    def test_per_request_verify_overrides_transport(self):
        session = _RecordingSession()
        transport = RequestsTransport(session=session, verify=False, timeout=NO_TIMEOUT)
        request = _get()
        request.verify = True

        transport.execute(request)

        self.assertTrue(session.calls[0][2]["verify"])

    def test_default_defers_so_a_custom_ca_bundle_survives(self):
        session = _RecordingSession()
        session.verify = "/etc/ssl/certs/ca.pem"

        RequestsTransport(session=session, timeout=NO_TIMEOUT).execute(_get())

        self.assertNotIn("verify", session.calls[0][2])

    def test_with_transport_forwards_verify_and_proxies(self):
        session = _RecordingSession()
        ctx = GraphClient().with_transport(
            session=session,
            verify=False,
            proxies={"https": "http://proxy:8080"},
            timeout=NO_TIMEOUT,
        )

        ctx.pending_request().transport.execute(_get())

        kwargs = session.calls[0][2]
        self.assertFalse(kwargs["verify"])
        self.assertEqual(kwargs["proxies"], {"https": "http://proxy:8080"})


if __name__ == "__main__":
    unittest.main()
