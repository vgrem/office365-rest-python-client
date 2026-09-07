"""Batch sizing: sub-request byte estimation, partition-by-limits, reject marker."""

from __future__ import annotations

from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.odata.batch_util import (
    WHOLE_BATCH_REJECT_CODES,
    WholeBatchRejected,
    estimate_query_bytes,
    partition_by_limits,
)


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
