"""Async runtime tests (offline).

Covers the transport foundation and the async query terminals: the default
:meth:`BaseTransport.execute_async` offloads the blocking transport to a worker
thread, and ``execute_query_async`` mirrors the synchronous request lifecycle
(hooks, response processing, error dispatch) without blocking the event loop.
"""

from __future__ import annotations

import asyncio
import threading
import time
from unittest import mock

import pytest
from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.v4.batch_request import ODataV4BatchRequest
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.queries.deferred import DeferredOperationQuery
from office365.runtime.transport.base import BaseTransport
from office365.sharepoint.client_context import ClientContext
from tests._scripted_transport import ScriptedTransport

_URL = "https://contoso.sharepoint.com/_api/web"
_SITE_URL = "https://contoso.sharepoint.com"


def _context(payloads: list) -> tuple[ClientContext, ScriptedTransport]:
    ctx = ClientContext(_SITE_URL)
    ctx.pending_request().beforeExecute.clear()
    transport = ScriptedTransport(payloads)
    ctx.pending_request().transport = transport
    return ctx, transport


def test_execute_async_returns_response() -> None:
    transport = ScriptedTransport([{"d": {"results": []}}])

    response = asyncio.run(transport.execute_async(RequestOptions(url=_URL)))

    assert response.status_code == 200  # noqa: PLR2004
    assert response.json() == {"d": {"results": []}}


def test_execute_async_offloads_to_worker_thread() -> None:
    """The default async path must not run the blocking execute() on the loop."""
    loop_thread = threading.get_ident()
    seen: dict[str, int] = {}

    class _ThreadRecordingTransport(BaseTransport):
        def execute(self, request: RequestOptions):
            seen["thread"] = threading.get_ident()
            return ScriptedTransport([{"d": {}}]).execute(request)

    transport = _ThreadRecordingTransport()
    asyncio.run(transport.execute_async(RequestOptions(url=_URL)))

    assert seen["thread"] != loop_thread


def test_context_execute_query_async_processes_response() -> None:
    ctx, transport = _context([{"d": {"Title": "Contoso"}}])
    ctx.load(ctx.web)

    asyncio.run(ctx.execute_query_async())

    assert ctx.web.properties.get("Title") == "Contoso"
    assert transport.calls == 1


def test_client_object_execute_query_async_chains() -> None:
    ctx, _ = _context([{"d": {"Title": "Contoso"}}])

    async def _run() -> object:
        return await ctx.web.execute_query_async()

    assert asyncio.run(_run()) is ctx.web


def test_deferred_query_resolves_without_request() -> None:
    ctx, transport = _context([])
    ctx.add_query(DeferredOperationQuery(ctx))

    asyncio.run(ctx.execute_query_async())

    assert transport.calls == 0


def test_execute_query_async_raises_on_http_error() -> None:
    ctx, _ = _context([{"status": 404, "body": {"error": {"message": "missing"}}}])
    ctx.load(ctx.web)

    with pytest.raises(ClientRequestException):
        asyncio.run(ctx.execute_query_async())


def test_execute_query_async_dispatches_to_on_error() -> None:
    ctx, _ = _context([{"status": 404, "body": {"error": {"message": "missing"}}}])
    handled: list[ClientRequestException] = []
    ctx.load(ctx.web)
    ctx.on_error(handled.append)

    asyncio.run(ctx.execute_query_async())

    assert len(handled) == 1


def test_execute_query_async_retry_recovers() -> None:
    ctx, transport = _context(
        [
            {"status": 429, "retry_after": 0, "body": {}},
            {"d": {"Title": "Contoso"}},
        ]
    )
    ctx.load(ctx.web)

    asyncio.run(ctx.execute_query_async_retry(max_retry=3, timeout_secs=0))

    assert ctx.web.properties.get("Title") == "Contoso"
    assert transport.calls == 2  # noqa: PLR2004


def test_execute_query_async_retry_exhausts() -> None:
    ctx, transport = _context([{"status": 500, "body": {}} for _ in range(3)])
    ctx.load(ctx.web)

    with pytest.raises(ClientRequestException):
        asyncio.run(ctx.execute_query_async_retry(max_retry=3, timeout_secs=0))

    assert transport.calls == 3  # noqa: PLR2004


def test_async_context_manager_closes_transport() -> None:
    closed: list[bool] = []

    class _ClosableTransport(ScriptedTransport):
        def close(self) -> None:
            closed.append(True)

    ctx = ClientContext(_SITE_URL)
    ctx.pending_request().transport = _ClosableTransport([])

    async def _run() -> None:
        async with ctx:
            pass

    asyncio.run(_run())

    assert closed == [True]


def test_clone_reuses_async_transport() -> None:
    """A clone keeps the explicitly configured async transport of its parent."""
    ctx = ClientContext(_SITE_URL)
    ctx.pending_request().beforeExecute.clear()
    async_transport = ScriptedTransport([{"d": {"Title": "Contoso"}}])
    ctx.pending_request().with_async_transport(async_transport)

    clone = ctx.clone(_SITE_URL)
    clone.pending_request().beforeExecute.clear()
    clone.load(clone.web)

    asyncio.run(clone.execute_query_async())

    assert clone.web.properties.get("Title") == "Contoso"
    assert async_transport.calls == 1


class _AsyncGraphBatchHarness(GraphClient):
    """GraphClient whose batch units are recorded instead of sent over HTTP."""

    def __init__(self) -> None:
        super().__init__()
        self.executed: list[object] = []
        self.thread_ids: list[int] = []
        self.max_active = 0
        self._active = 0
        self._lock = threading.Lock()

    def _execute_batch(self, batch_qry):
        with self._lock:
            self._active += 1
            self.max_active = max(self.max_active, self._active)
        time.sleep(0.02)
        with self._lock:
            self._active -= 1
        self.executed.append(batch_qry)
        self.thread_ids.append(threading.get_ident())
        return [batch_qry]


def _enqueue(ctx: GraphClient, count: int) -> None:
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().authenticate_request = lambda request: None  # type: ignore[method-assign]
    for _ in range(count):
        ctx.add_query(ClientQuery(ctx))


def test_execute_batch_async_runs_batches_concurrently() -> None:
    ctx = _AsyncGraphBatchHarness()
    _enqueue(ctx, 4)
    results: list[list] = []

    asyncio.run(ctx.execute_batch_async(items_per_batch=1, concurrency=4, success_callback=results.append))

    assert len(results) == 4  # noqa: PLR2004
    assert len(ctx.executed) == 4  # noqa: PLR2004
    assert ctx.max_active > 1


def test_execute_batch_async_offloads_off_loop_thread() -> None:
    loop_thread = threading.get_ident()
    ctx = _AsyncGraphBatchHarness()
    _enqueue(ctx, 1)

    asyncio.run(ctx.execute_batch_async(items_per_batch=1))

    assert ctx.thread_ids and ctx.thread_ids[0] != loop_thread


def test_execute_batch_async_raises_first_error() -> None:
    ctx = _AsyncGraphBatchHarness()

    def _boom(batch_qry):
        raise RuntimeError("boom")

    ctx._execute_batch = _boom  # type: ignore[method-assign]
    _enqueue(ctx, 2)
    results: list[list] = []

    with pytest.raises(RuntimeError):
        asyncio.run(ctx.execute_batch_async(items_per_batch=1, concurrency=2, success_callback=results.append))

    assert results == []


def test_execute_batch_async_rejects_sequential_with_concurrency() -> None:
    ctx = GraphClient()

    with pytest.raises(ValueError):
        asyncio.run(ctx.execute_batch_async(sequential=True, concurrency=2))


def test_graph_execute_batch_async_end_to_end() -> None:
    ctx = GraphClient()
    _enqueue(ctx, 1)
    transport = ScriptedTransport([{"responses": [{"id": "0", "status": 200, "headers": {}, "body": {}}]}])
    real_cls = ODataV4BatchRequest

    def _factory(*args, **kwargs):
        batch_request = real_cls(*args, **kwargs)
        batch_request.transport = transport
        return batch_request

    with mock.patch("office365.graph_client.ODataV4BatchRequest", side_effect=_factory):
        asyncio.run(ctx.execute_batch_async(items_per_batch=1))

    assert transport.calls == 1


def test_sharepoint_execute_batch_async_warms_up_and_splits() -> None:
    ctx = ClientContext(_SITE_URL)
    warmed: list[bool] = []
    ctx.pending_request().warm_up = lambda: warmed.append(True)  # type: ignore[method-assign]
    seen: list[object] = []

    def _record(batch_qry):
        seen.append(batch_qry)
        return [batch_qry]

    ctx._execute_batch = _record  # type: ignore[method-assign]
    _enqueue(ctx, 2)

    asyncio.run(ctx.execute_batch_async(items_per_batch=1, concurrency=2))

    assert warmed == [True]
    assert len(seen) == 2  # noqa: PLR2004
