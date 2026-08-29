"""Offline tests for the data-pipeline foundation: records, NDJSON, Excel, progress."""

# ruff: noqa: E402  (imports must follow the importorskip guard)

from __future__ import annotations

import io
from typing import cast

import pytest

openpyxl = pytest.importorskip("openpyxl")

from office365.directory.users.user import User
from office365.graph_client import GraphClient
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.converters.excel import read_excel, write_excel
from office365.runtime.converters.ndjson import read_ndjson, write_ndjson
from office365.runtime.operations import Progress, query_progress_hook
from office365.runtime.queries.client_query import ClientQuery


def _collection(properties: list[dict], context=None) -> ClientObjectCollection:
    col = ClientObjectCollection(context or cast(ClientRuntimeContext, None), User, None)
    for props in properties:
        col.add_child(col.create_typed_object(props))
    return col


def test_progress_percent():
    assert Progress(done=0, total=0).percent is None
    assert Progress(done=0, total=None).percent is None
    assert Progress(done=5, total=10).percent == 50.0  # noqa: PLR2004
    assert Progress(done=12, total=10).percent == 100.0  # noqa: PLR2004


def test_to_records():
    col = _collection(
        [
            {"userPrincipalName": "jdoe@x.com", "displayName": "John Doe", "accountEnabled": True},
        ]
    )
    col.query_options.select = ["displayName", "userPrincipalName"]
    assert col.to_records() == [{"displayName": "John Doe", "userPrincipalName": "jdoe@x.com"}]


def test_from_records_queues_creates():
    client = GraphClient()
    col = ClientObjectCollection(client, User, None)
    col.from_records([{"userPrincipalName": "jdoe@x.com", "displayName": "John"}])
    assert len(col) == 1
    assert len(client._queries) == 1


def test_from_records_strips_non_importable():
    client = GraphClient()
    col = ClientObjectCollection(client, User, None)
    col.from_records([{"userPrincipalName": "jdoe@x.com", "id": "42", "@odata.type": "user"}])
    item = col[0]
    assert item.get_property("userPrincipalName") == "jdoe@x.com"
    assert "id" not in item.properties
    assert "@odata.type" not in item.properties


def test_ndjson_round_trip():
    records = [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]
    buf = io.StringIO()
    write_ndjson(records, buf)
    assert read_ndjson(io.StringIO(buf.getvalue())) == records


def test_json_file_round_trip():
    import json as jsonlib

    from office365.runtime.converters.json_file import read_json, write_json

    records = [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]
    buf = io.StringIO()
    write_json(records, buf)
    assert jsonlib.loads(buf.getvalue()) == records
    assert read_json(io.StringIO(buf.getvalue())) == records


def test_from_json_file_queues_creates(tmp_path):
    import json as jsonlib

    path = tmp_path / "data.json"
    path.write_text(jsonlib.dumps([{"userPrincipalName": "jdoe@x.com", "id": "42", "noSuchColumn": "x"}]))
    client = GraphClient()
    col = ClientObjectCollection(client, User, None)
    col.from_json_file(open(path))  # noqa: SIM115
    assert len(col) == 1
    item = col[0]
    assert item.get_property("userPrincipalName") == "jdoe@x.com"
    assert "id" not in item.properties
    assert "noSuchColumn" not in item.properties


def test_excel_round_trip(tmp_path):
    records = [{"Name": "John", "Age": 30}, {"Name": "Alice", "Age": 25}]
    path = str(tmp_path / "out.xlsx")
    write_excel(records, path)
    assert read_excel(path) == records


def test_query_progress_hook():
    events = []
    hook = query_progress_hook(3, lambda p: events.append(p), stage="importing")
    for _ in range(3):
        hook(None)  # each call mimics one queued query completing
    assert [p.done for p in events] == [1, 2, 3]  # noqa: PLR2004
    assert all(p.total == 3 for p in events)  # noqa: PLR2004
    assert all(p.stage == "importing" for p in events)
    assert events[-1].percent == 100.0  # noqa: PLR2004


def test_deferred_operation_query():
    from office365.runtime.queries.deferred import DeferredOperationQuery

    client = GraphClient()
    barrier = DeferredOperationQuery(client)
    client.add_query(barrier)

    add = ClientQuery(client)
    barrier.defer(add)  # swaps the placeholder's slot for the real query
    assert list(client._queries) == [add]

    client2 = GraphClient()
    barrier2 = DeferredOperationQuery(client2)
    client2.add_query(barrier2)
    barrier2.resolve()  # no operation needed — drops the placeholder
    assert list(client2._queries) == []


class _FakeRequest:
    def __init__(self):
        self.executed = []
        self.after_execute_calls = 0

    def execute_query(self, qry):
        self.executed.append(qry)

    def afterExecute(self, _response):
        self.after_execute_calls += 1


def test_deferred_execute_query_noop():
    from office365.runtime.queries.deferred import DeferredOperationQuery

    client = GraphClient()
    barrier = DeferredOperationQuery(client)
    request = _FakeRequest()
    barrier.execute_query(request)  # no-op resolve: fires after_execute, sends no request
    assert request.after_execute_calls == 1
    assert request.executed == []


def test_deferred_execute_query_runs_operation():
    from office365.runtime.queries.deferred import DeferredOperationQuery

    client = GraphClient()
    barrier = DeferredOperationQuery(client)
    op = ClientQuery(client)
    barrier.defer(op)
    request = _FakeRequest()
    barrier.execute_query(request)  # deferred: runs the operation via the request
    assert request.executed == [op]


def test_ensure_property_cached_queues_deferred_noop():
    user = GraphClient().users["123"]
    user.set_property("id", "123")
    user.set_property("displayName", "John Doe")
    user.ensure_property("displayName")  # already loaded — no redundant GET
    from office365.runtime.queries.deferred import DeferredOperationQuery

    assert isinstance(user.context._queries[-1], DeferredOperationQuery)


def test_get_all_accepts_progress():
    client = GraphClient()
    col = ClientObjectCollection(client, User, None)
    events = []
    col.get_all(progress=lambda p: events.append(p))
    assert len(client._queries) >= 1  # the first page query is queued


def test_from_records_accepts_progress():
    client = GraphClient()
    col = ClientObjectCollection(client, User, None)
    col.from_records(
        [{"userPrincipalName": "jdoe@x.com"}, {"userPrincipalName": "asmith@x.com"}],
        progress=lambda p: None,
    )
    assert len(col) == 2  # noqa: PLR2004
    assert len(client._queries) == 2  # noqa: PLR2004
