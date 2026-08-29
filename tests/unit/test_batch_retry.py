"""Offline tests for per-sub-request batch retry (only failed sub-requests re-sent)."""

from __future__ import annotations

import json as jsonlib
import unittest
from unittest import mock

from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.odata.v4.batch_request import ODataV4BatchRequest
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.queries.batch import BatchQuery
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.transport.base import BaseTransport
from requests import Response


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

        with mock.patch("office365.runtime.odata.v4.batch_request.sleep"):
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

        with mock.patch("office365.runtime.odata.v4.batch_request.sleep"):
            with self.assertRaises(ClientRequestException):
                req.execute_query_with_retry(_make_batch(client, 1), max_retry=2, base_delay=1, jitter=False)

        self.assertEqual(transport.calls, 2)

    def test_honors_longest_retry_after(self):
        client = GraphClient()
        transport = _FakeTransport([_envelope([429, 429], retry_after=7), _envelope([200, 200])])
        req = ODataV4BatchRequest("", V4JsonFormat())
        req.transport = transport

        with mock.patch("office365.runtime.odata.v4.batch_request.sleep") as sleep_mock:
            req.execute_query_with_retry(_make_batch(client, 2), max_retry=3, jitter=False)

        sleep_mock.assert_called_once_with(7)


if __name__ == "__main__":
    unittest.main()
