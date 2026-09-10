"""Merged unit tests (consolidated; see git history for originals)."""

from __future__ import annotations

import json as jsonlib
import threading
import time
import unittest
from unittest import mock

from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.odata.batch_util import (
    WHOLE_BATCH_REJECT_CODES,
    WholeBatchRejected,
    estimate_query_bytes,
    partition_by_limits,
)
from office365.runtime.odata.v4.batch_request import ODataV4BatchRequest
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.queries.batch import BatchQuery
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.transport.base import BaseTransport
from office365.sharepoint.client_context import ClientContext
from requests import Response


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


def _envelope(sub_statuses: list[int], retry_after: int | None = None) -> dict:
    responses = []
    for index, status in enumerate(sub_statuses):
        sub = {"id": str(index), "status": status, "headers": {}, "body": {}}
        if status == 429:  # noqa: PLR2004
            sub["headers"]["Retry-After"] = str(retry_after or 1)
            sub["body"] = {"error": {"code": "TooManyRequests", "message": "slow down"}}
        responses.append(sub)
    return {"responses": responses}


class _FakeTransport(BaseTransport):
    def __init__(self, payloads: list[dict]) -> None:
        self._payloads = payloads
        self.calls = 0
        self.request_payloads: list[dict] = []

    def execute(self, request):
        payload = self._payloads[min(self.calls, len(self._payloads) - 1)]
        self.calls += 1
        self.request_payloads.append(request.data)
        resp = Response()
        resp.status_code = 200
        resp.url = request.url
        resp._content = jsonlib.dumps(payload).encode("utf-8")
        return resp


def _make_batch(client: GraphClient, count: int) -> BatchQuery:
    client.pending_request().beforeExecute.clear()  # no auth handler during offline payload build
    return BatchQuery(client, [ClientQuery(client) for _ in range(count)])


class TestBatchSubRequestRetry(unittest.TestCase):
    def test_retries_only_failed_subrequests(self):
        client = GraphClient()
        transport = _FakeTransport([_envelope([200, 429], retry_after=1), _envelope([200])])
        req = ODataV4BatchRequest("", V4JsonFormat())
        req.transport = transport

        with mock.patch("office365.runtime.retry.sleep"):
            req.execute_query_with_retry(_make_batch(client, 2), max_retry=3, base_delay=1, jitter=False)

        # two batch round-trips: the full batch, then only the failed sub-request
        self.assertEqual(transport.calls, 2)
        self.assertEqual(len(transport.request_payloads[0]["requests"]), 2)
        self.assertEqual(len(transport.request_payloads[1]["requests"]), 1)

    def test_succeeds_on_first_round_trip(self):
        client = GraphClient()
        transport = _FakeTransport([_envelope([200, 200])])
        req = ODataV4BatchRequest("", V4JsonFormat())
        req.transport = transport

        req.execute_query_with_retry(_make_batch(client, 2), max_retry=3)

        self.assertEqual(transport.calls, 1)

    def test_non_transient_sub_failure_raises_without_retry(self):
        client = GraphClient()
        transport = _FakeTransport([_envelope([200, 400])])
        req = ODataV4BatchRequest("", V4JsonFormat())
        req.transport = transport

        with self.assertRaises(ClientRequestException):
            req.execute_query_with_retry(_make_batch(client, 2), max_retry=3)

        self.assertEqual(transport.calls, 1)

    def test_retries_exhausted_raises(self):
        client = GraphClient()
        transport = _FakeTransport([_envelope([429]), _envelope([429]), _envelope([429])])
        req = ODataV4BatchRequest("", V4JsonFormat())
        req.transport = transport

        with mock.patch("office365.runtime.retry.sleep"):
            with self.assertRaises(ClientRequestException):
                req.execute_query_with_retry(_make_batch(client, 1), max_retry=2, base_delay=1, jitter=False)

        self.assertEqual(transport.calls, 2)

    def test_honors_longest_retry_after(self):
        client = GraphClient()
        transport = _FakeTransport([_envelope([429, 429], retry_after=7), _envelope([200, 200])])
        req = ODataV4BatchRequest("", V4JsonFormat())
        req.transport = transport

        with mock.patch("office365.runtime.retry.sleep") as sleep_mock:
            req.execute_query_with_retry(_make_batch(client, 2), max_retry=3, jitter=False)

        sleep_mock.assert_called_once_with(7)


class _FakeQuery:
    def __init__(self, url: str, payload: dict | str | None = None, headers: dict | None = None):
        self.url = url
        self.parameters_type = payload
        self.custom_headers = headers or {}


def test_estimate_query_bytes():
    big = _FakeQuery("https://x/site/_api/web/lists/guid/items(1)", {"title": "x" * 5000})
    small = _FakeQuery("https://x/site/_api/web/lists/guid/items(1)", None)
    assert estimate_query_bytes(big) > estimate_query_bytes(small)


def test_partition_respects_item_cap():
    queries = [_FakeQuery("u") for _ in range(7)]
    batches = partition_by_limits(queries, max_items=3, max_bytes=None)
    assert [len(b) for b in batches] == [3, 3, 1]
    assert [q.url for q in batches[0]] == ["u", "u", "u"]  # order preserved


def test_partition_respects_byte_cap():
    queries = [
        _FakeQuery("u", {"data": "a" * 100}),
        _FakeQuery("u", {"data": "b" * 100}),
        _FakeQuery("u", {"data": "c" * 100}),
    ]
    batches = partition_by_limits(queries, max_items=None, max_bytes=estimate_query_bytes(queries[0]) * 2 + 200)
    assert len(batches) >= 2  # noqa: PLR2004 — big payloads don't all land in one batch


def test_oversized_single_stays_alone():
    huge = _FakeQuery("u", {"data": "x" * 100000})
    queries = [huge, _FakeQuery("u", None)]
    batches = partition_by_limits(queries, max_items=None, max_bytes=1000)
    assert len(batches) == 2  # noqa: PLR2004
    assert len(batches[0]) == 1


def test_whole_batch_reject_marker_carries_queries_and_cause():
    cause = ClientRequestException("400 body too large")
    reject = WholeBatchRejected([_FakeQuery("u")], cause)
    assert len(reject.queries) == 1
    assert reject.__cause__ is cause
    assert 413 in WHOLE_BATCH_REJECT_CODES  # noqa: PLR2004
