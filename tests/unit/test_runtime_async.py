"""Async runtime tests (offline).

Covers the transport foundation and the async query terminals: the default
:meth:`BaseTransport.execute_async` offloads the blocking transport to a worker
thread, and ``execute_query_async`` mirrors the synchronous request lifecycle
(hooks, response processing, error dispatch) without blocking the event loop.
"""

from __future__ import annotations

import asyncio
import threading
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
from requests import Response
from tests._scripted_transport import AsyncScriptedTransport, ScriptedTransport

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

    async def _execute_batch_async(self, batch_qry):
        with self._lock:
            self._active += 1
            self.max_active = max(self.max_active, self._active)
        try:
            await asyncio.sleep(0.02)
            self.executed.append(batch_qry)
            self.thread_ids.append(threading.get_ident())
            return [batch_qry]
        finally:
            with self._lock:
                self._active -= 1


class _ThreadRecordingTransport(ScriptedTransport):
    """Transport that records the thread its (blocking) send runs on."""

    def __init__(self, payloads: list) -> None:
        super().__init__(payloads)
        self.threads: list[int] = []

    def execute(self, request):
        self.threads.append(threading.get_ident())
        return super().execute(request)


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
    """The real Graph async batch sends through the configured async transport."""
    loop_thread = threading.get_ident()
    ctx = GraphClient()
    _enqueue(ctx, 1)
    transport = _ThreadRecordingTransport([{"responses": [{"id": "0", "status": 200, "headers": {}, "body": {}}]}])
    ctx.pending_request().with_async_transport(transport)

    asyncio.run(ctx.execute_batch_async(items_per_batch=1))

    assert transport.threads and transport.threads[0] != loop_thread


def test_execute_batch_async_raises_first_error() -> None:
    ctx = _AsyncGraphBatchHarness()

    async def _boom(batch_qry):
        raise RuntimeError("boom")

    ctx._execute_batch_async = _boom  # type: ignore[method-assign]
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


def test_graph_execute_batch_async_native_transport_end_to_end() -> None:
    """The async batch runs through a transport that only implements ``execute_async``."""
    ctx = GraphClient()
    _enqueue(ctx, 1)
    transport = AsyncScriptedTransport([{"responses": [{"id": "0", "status": 200, "headers": {}, "body": {}}]}])
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

    async def _record(batch_qry):
        seen.append(batch_qry)
        return [batch_qry]

    ctx._execute_batch_async = _record  # type: ignore[method-assign]
    _enqueue(ctx, 2)

    asyncio.run(ctx.execute_batch_async(items_per_batch=1, concurrency=2))

    assert warmed == [True]
    assert len(seen) == 2  # noqa: PLR2004


class _ConcurrencyTrackingTransport(AsyncScriptedTransport):
    """Native-async transport that records the peak number of in-flight requests."""

    def __init__(self, payloads: list) -> None:
        super().__init__(payloads)
        self.active = 0
        self.max_active = 0

    async def execute_async(self, request):
        self.active += 1
        self.max_active = max(self.max_active, self.active)
        await asyncio.sleep(0.02)
        response = await super().execute_async(request)
        self.active -= 1
        return response


def _queue_loads(ctx: ClientContext, count: int) -> None:
    for _ in range(count):
        ctx.load(ctx.web)


def _sp_page(items: list) -> dict:
    return {"d": {"results": [{"Id": i, "Title": f"Item {i}"} for i in items]}}


def test_get_all_async_pages_until_exhausted() -> None:
    ctx = ClientContext(_SITE_URL)
    transport = ScriptedTransport([_sp_page([1, 2]), _sp_page([3, 4]), _sp_page([])])
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = transport
    seen: list[int] = []
    col = ctx.web.lists

    asyncio.run(col.get_all_async(page_size=2, progress=lambda p: seen.append(p.done)))

    assert [lst.properties.get("Id") for lst in col] == [1, 2, 3, 4]
    assert transport.calls == 3  # noqa: PLR2004
    assert seen == [2, 4, 4]
    assert not ctx.has_pending_request


def test_get_all_async_follows_next_link() -> None:
    next_url = "https://graph.microsoft.com/v1.0/users?$skiptoken=abc"
    ctx = GraphClient()
    ctx.pending_request().beforeExecute.clear()
    transport = ScriptedTransport(
        [
            {"@odata.nextLink": next_url, "value": [{"id": "1"}, {"id": "2"}]},
            {"value": [{"id": "3"}]},
        ]
    )
    ctx.pending_request().transport = transport
    loaded: list[int] = []
    col = ctx.users

    asyncio.run(col.get_all_async(page_size=2, page_loaded=lambda _col: loaded.append(1)))

    assert [u.properties.get("id") for u in col] == ["1", "2", "3"]
    assert transport.calls == 2  # noqa: PLR2004
    assert loaded == [1, 1]


def test_aiter_fetches_pages_lazily() -> None:
    """``async for`` pulls pages on demand, without a prior ``get_all_async``."""
    ctx = ClientContext(_SITE_URL)
    transport = ScriptedTransport([_sp_page([1, 2]), _sp_page([3, 4]), _sp_page([])])
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = transport
    col = ctx.web.lists

    async def _collect() -> list:
        return [lst.properties.get("Id") async for lst in col.paged(page_size=2)]

    assert asyncio.run(_collect()) == [1, 2, 3, 4]  # noqa: PLR2004
    assert transport.calls == 3  # noqa: PLR2004


def test_aiter_follows_next_link() -> None:
    """``async for`` follows a server-driven ``@odata.nextLink``."""
    next_url = "https://graph.microsoft.com/v1.0/users?$skiptoken=abc"
    ctx = GraphClient()
    ctx.pending_request().beforeExecute.clear()
    transport = ScriptedTransport(
        [
            {"@odata.nextLink": next_url, "value": [{"id": "1"}, {"id": "2"}]},
            {"value": [{"id": "3"}]},
        ]
    )
    ctx.pending_request().transport = transport
    col = ctx.users

    async def _collect() -> list:
        return [u.properties.get("id") async for u in col]

    assert asyncio.run(_collect()) == ["1", "2", "3"]
    assert transport.calls == 2  # noqa: PLR2004


def test_aiter_iterates_loaded_items_without_refetch() -> None:
    ctx = ClientContext(_SITE_URL)
    transport = ScriptedTransport([_sp_page([1, 2]), _sp_page([])])
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = transport
    col = ctx.web.lists

    async def _collect() -> list:
        await col.get_all_async(page_size=2)
        calls_after_load = transport.calls
        ids = [lst.properties.get("Id") async for lst in col]
        assert transport.calls == calls_after_load  # iteration does not refetch
        return ids

    assert asyncio.run(_collect()) == [1, 2]


def test_execute_query_parallel_async_overlaps_requests() -> None:
    transport = _ConcurrencyTrackingTransport([{"d": {"Title": "Contoso"}}] * 4)
    ctx = ClientContext(_SITE_URL)
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = transport
    _queue_loads(ctx, 4)

    asyncio.run(ctx.execute_query_parallel_async(concurrency=4))

    assert transport.calls == 4  # noqa: PLR2004
    assert transport.max_active > 1
    assert ctx.web.properties.get("Title") == "Contoso"


def test_execute_query_parallel_async_processes_in_order_and_reports_progress() -> None:
    ctx, transport = _context([{"d": {"Title": f"T{i}"}} for i in range(3)])
    _queue_loads(ctx, 3)
    seen: list = []

    asyncio.run(ctx.execute_query_parallel_async(concurrency=3, progress=seen.append))

    assert [p.done for p in seen] == [1, 2, 3]
    assert seen[-1].total == 3  # noqa: PLR2004
    assert seen[-1].stage == "parallel"
    assert transport.calls == 3  # noqa: PLR2004


def test_execute_query_parallel_async_retries_transient() -> None:
    ctx, transport = _context(
        [
            {"status": 429, "retry_after": 0, "body": {}},
            {"d": {"Title": "Contoso"}},
        ]
    )
    ctx.load(ctx.web)

    asyncio.run(ctx.execute_query_parallel_async(concurrency=2, max_retry=3, timeout_secs=0))

    assert ctx.web.properties.get("Title") == "Contoso"
    assert transport.calls == 2  # noqa: PLR2004


def test_execute_query_parallel_async_raises_on_permanent_error() -> None:
    ctx, transport = _context([{"status": 404, "body": {"error": {"message": "missing"}}}])
    ctx.load(ctx.web)

    with pytest.raises(ClientRequestException):
        asyncio.run(ctx.execute_query_parallel_async(concurrency=2))

    assert transport.calls == 1


def test_execute_query_parallel_async_requeues_exhausted_transient() -> None:
    ctx, transport = _context([{"status": 500, "body": {}}])
    ctx.load(ctx.web)

    with pytest.raises(ClientRequestException):
        asyncio.run(ctx.execute_query_parallel_async(concurrency=2, max_retry=1, timeout_secs=0))

    assert transport.calls == 1
    assert ctx.has_pending_request  # failed query kept for a retry


def test_execute_query_parallel_async_concurrency_one_falls_back() -> None:
    ctx, transport = _context([{"d": {"Title": "Contoso"}}])
    ctx.load(ctx.web)

    asyncio.run(ctx.execute_query_parallel_async(concurrency=1))

    assert ctx.web.properties.get("Title") == "Contoso"
    assert transport.calls == 1


def test_execute_query_parallel_async_empty_queue_is_noop() -> None:
    ctx, transport = _context([])

    asyncio.run(ctx.execute_query_parallel_async(concurrency=4))

    assert transport.calls == 0
    assert not ctx.has_pending_request


def test_execute_query_parallel_on_error_collects_and_continues() -> None:
    """A permanent failure is reported and skipped instead of aborting the batch."""
    ctx, transport = _context(
        [
            {"status": 404, "body": {"error": {"message": "missing"}}},
            {"d": {"Title": "Contoso"}},
        ]
    )
    _queue_loads(ctx, 2)
    errors: list[BaseException] = []

    ctx.execute_query_parallel(concurrency=2, on_error=lambda _qry, error: errors.append(error))

    assert len(errors) == 1
    assert isinstance(errors[0], ClientRequestException)
    assert ctx.web.properties.get("Title") == "Contoso"
    assert transport.calls == 2  # noqa: PLR2004
    assert not ctx.has_pending_request  # failed query is not re-queued


def test_execute_query_parallel_async_on_error_collects_and_continues() -> None:
    ctx, transport = _context(
        [
            {"status": 404, "body": {"error": {"message": "missing"}}},
            {"d": {"Title": "Contoso"}},
        ]
    )
    _queue_loads(ctx, 2)
    errors: list[BaseException] = []

    asyncio.run(ctx.execute_query_parallel_async(concurrency=2, on_error=lambda _qry, error: errors.append(error)))

    assert len(errors) == 1
    assert isinstance(errors[0], ClientRequestException)
    assert ctx.web.properties.get("Title") == "Contoso"
    assert transport.calls == 2  # noqa: PLR2004
    assert not ctx.has_pending_request


def test_execute_query_parallel_on_error_honored_with_concurrency_one() -> None:
    """With an on_error collector, concurrency=1 must not fall back to raising."""
    ctx, transport = _context([{"status": 404, "body": {"error": {"message": "missing"}}}])
    ctx.load(ctx.web)
    errors: list[BaseException] = []

    ctx.execute_query_parallel(concurrency=1, on_error=lambda _qry, error: errors.append(error))

    assert len(errors) == 1
    assert transport.calls == 1
    assert not ctx.has_pending_request


def test_execute_query_async_offloads_before_execute_hooks() -> None:
    """Blocking ``beforeExecute`` hooks (auth/digest) run off the loop thread."""
    loop_thread = threading.get_ident()
    ctx, transport = _context([{"d": {"Title": "Contoso"}}])
    hook_threads: list[int] = []

    def _hook(_request: RequestOptions) -> None:
        hook_threads.append(threading.get_ident())

    ctx.pending_request().before_execute(_hook, once=False)
    ctx.load(ctx.web)

    asyncio.run(ctx.execute_query_async())

    assert hook_threads and hook_threads[0] != loop_thread
    assert ctx.web.properties.get("Title") == "Contoso"


class _CancellingTransport(AsyncScriptedTransport):
    """Native-async transport that cancels the in-flight request (simulated)."""

    def __init__(self) -> None:
        super().__init__([])
        self.started = 0

    async def execute_async(self, request):
        self.started += 1
        raise asyncio.CancelledError


def test_execute_query_parallel_async_restores_pending_on_cancellation() -> None:
    """Cancellation mid-flight re-queues the unapplied queries and clears state."""
    transport = _CancellingTransport()
    ctx = ClientContext(_SITE_URL)
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = transport
    _queue_loads(ctx, 3)

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(ctx.execute_query_parallel_async(concurrency=3))

    assert ctx.has_pending_request
    assert len(ctx._queries) == 3  # noqa: PLR2004
    assert ctx._current_query is None


def test_observe_throttle_prefers_recorded_limiter() -> None:
    """A batch request observes sub-responses via its recorded limiter."""
    ctx = ClientContext(_SITE_URL)
    request = ctx.pending_request()
    limiter = mock.Mock()
    request._rate_limiter = limiter
    response = Response()
    response.status_code = 200  # noqa: PLR2004

    request._observe_throttle(response)

    limiter.observe.assert_called_once_with(response)
