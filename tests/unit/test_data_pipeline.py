"""Merged unit tests (consolidated; see git history for originals)."""

from __future__ import annotations

import io
import unittest
import warnings
from datetime import datetime, timezone
from typing import cast

import pytest
from office365.directory.users.user import User
from office365.graph_client import GraphClient
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.converters.csv_reader import coerce_records, read_csv_records
from office365.runtime.converters.csv_writer import write_csv
from office365.runtime.converters.dataframe import (
    DataFrameResult,
    read_dataframe,
    records_from_dataframe,
    series_kind,
    write_dataframe,
)
from office365.runtime.converters.excel import read_excel, write_excel
from office365.runtime.converters.ndjson import read_ndjson, write_ndjson
from office365.runtime.operations import query_progress_hook
from office365.runtime.queries.client_query import ClientQuery
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.collection import field_type_from_kind
from office365.sharepoint.fields.type import FieldType
from office365.sharepoint.listitems.collection import ListItemCollection
from office365.sharepoint.listitems.listitem import ListItem
from tests import test_site_url
from tests.settings import cert_path, cert_thumbprint, client_id, tenant

CSV_TEXT = (
    "userPrincipalName,givenName,displayName,accountEnabled,officeLocation,"
    "passwordProfile/password,passwordProfile/forceChangePasswordNextSignIn,businessPhones\n"
    "jdoe@contoso.com,John,John Doe,True,Seattle,S3cret!,True,+1-555-0101; +1-555-0102\n"
)


def _graph_client() -> GraphClient:
    with open(cert_path, "r", encoding="utf-8") as f:
        private_key = f.read()
    return GraphClient(tenant=tenant).with_certificate(client_id, cert_thumbprint, private_key)


class TestCsvRecords(unittest.TestCase):
    def test_read_csv_records(self):
        records = read_csv_records(io.StringIO(CSV_TEXT))
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record["userPrincipalName"], "jdoe@contoso.com")
        self.assertEqual(record["passwordProfile/password"], "S3cret!")

    def test_coerce_records(self):
        records = coerce_records(
            User,
            read_csv_records(io.StringIO(CSV_TEXT)),
        )
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record["userPrincipalName"], "jdoe@contoso.com")
        self.assertEqual(record["passwordProfile"], {"password": "S3cret!", "forceChangePasswordNextSignIn": "True"})
        self.assertEqual(record["businessPhones"], ["+1-555-0101", "+1-555-0102"])

    def test_coerce_records_strips_non_importable_and_unknown(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            records = coerce_records(
                User,
                [
                    {
                        "userPrincipalName": "jdoe@contoso.com",
                        "id": "42",
                        "@odata.type": "user",
                        "noSuchColumn": "x",
                    }
                ],
            )
        self.assertEqual(records, [{"userPrincipalName": "jdoe@contoso.com"}])
        self.assertTrue(any("noSuchColumn" in str(w.message) for w in caught))


class TestImportPipeline(unittest.TestCase):
    def test_from_csv_queues_creates(self):
        client = _graph_client()
        users = client.users.from_csv(io.StringIO(CSV_TEXT))
        self.assertEqual(len(users), 1)
        self.assertEqual(len(client._queries), 1)
        user = users[0]
        self.assertIs(user.get_property("accountEnabled"), True)
        self.assertEqual(user.get_property("passwordProfile").password, "S3cret!")
        self.assertIs(user.get_property("passwordProfile").forceChangePasswordNextSignIn, True)
        self.assertEqual(list(user.get_property("businessPhones")), ["+1-555-0101", "+1-555-0102"])

    def test_from_json_queues_creates(self):
        client = _graph_client()
        users = client.users.from_json(
            [
                {
                    "userPrincipalName": "jdoe@contoso.com",
                    "displayName": "John Doe",
                    "accountEnabled": True,
                    "id": "42",
                    "@odata.type": "user",
                }
            ]
        )
        self.assertEqual(len(users), 1)
        self.assertEqual(len(client._queries), 1)
        self.assertIs(users[0].get_property("accountEnabled"), True)
        self.assertNotIn("id", users[0].properties)

    def test_round_trip_write_then_read(self):
        col = ClientObjectCollection(cast(ClientRuntimeContext, None), User, None)
        item = col.create_typed_object(
            {
                "userPrincipalName": "jdoe@contoso.com",
                "displayName": "John Doe",
                "accountEnabled": True,
                "createdDateTime": datetime(2025, 1, 15, 12, 34, 56, tzinfo=timezone.utc),
                "businessPhones": ["+1-555-0101", "+1-555-0102"],
            }
        )
        col.add_child(item)
        col.query_options.select = [
            "userPrincipalName",
            "displayName",
            "accountEnabled",
            "createdDateTime",
            "businessPhones",
        ]
        out = io.StringIO()
        write_csv(col, out)

        client = _graph_client()
        users = client.users.from_csv(io.StringIO(out.getvalue()))
        user = users[0]
        self.assertIs(user.get_property("accountEnabled"), True)
        self.assertEqual(user.get_property("createdDateTime"), datetime(2025, 1, 15, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(list(user.get_property("businessPhones")), ["+1-555-0101", "+1-555-0102"])


def test_list_item_keeps_unknown_columns_when_allowed():
    """List item columns are per-list metadata, so imports opt into unknown keys."""
    records = coerce_records(
        ListItem,
        [{"Title": "row", "CustomColumn": 42, "id": "x", "@odata.type": "u"}],
        allow_unknown=True,
    )
    assert records == [{"Title": "row", "CustomColumn": 42}]


def test_list_item_collection_from_records_keeps_custom_columns():
    ctx = ClientContext(test_site_url)
    col = ListItemCollection(ctx)
    col.from_records([{"Title": "row", "CustomColumn": 42}])

    assert len(col) == 1
    assert col[0].get_property("CustomColumn") == 42  # noqa: PLR2004
    assert col[0].get_property("Title") == "row"


def test_typed_entity_skips_unknown_columns():
    """Typed Graph entities still skip undeclared columns with a warning."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        records = coerce_records(User, [{"displayName": "John", "NotAProperty": 1}])

    assert records == [{"displayName": "John"}]
    assert any("Skipping unknown column" in str(w.message) for w in caught)


# ruff: noqa: E402  (imports must follow the importorskip guard)


openpyxl = pytest.importorskip("openpyxl")


def pipeline__collection(properties: list[dict], context=None) -> ClientObjectCollection:
    col = ClientObjectCollection(context or cast(ClientRuntimeContext, None), User, None)
    for props in properties:
        col.add_child(col.create_typed_object(props))
    return col


def test_to_records():
    col = pipeline__collection(
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


# ruff: noqa: E402  (imports must follow the importorskip guard)


pd = pytest.importorskip("pandas")


def pandas__collection(properties: list[dict], context=None) -> ClientObjectCollection:
    col = ClientObjectCollection(context or cast(ClientRuntimeContext, None), User, None)
    for props in properties:
        col.add_child(col.create_typed_object(props))
    return col


def test_write_dataframe():
    col = pandas__collection(
        [
            {"userPrincipalName": "jdoe@contoso.com", "displayName": "John Doe", "accountEnabled": True},
            {"userPrincipalName": "asmith@contoso.com", "displayName": "Alice Smith", "accountEnabled": False},
        ]
    )
    col.query_options.select = ["displayName", "userPrincipalName", "accountEnabled"]

    target = DataFrameResult(cast(ClientRuntimeContext, None))
    write_dataframe(col, target)

    df = target.value
    assert isinstance(target, DataFrameResult)
    assert list(df.columns) == ["displayName", "userPrincipalName", "accountEnabled"]
    assert df.iloc[0]["userPrincipalName"] == "jdoe@contoso.com"
    assert df.iloc[0]["accountEnabled"] == True  # noqa: E712  (numpy bool)


def test_read_dataframe_records():
    df = pd.DataFrame({"displayName": ["John"], "userPrincipalName": ["jdoe@contoso.com"]})
    assert read_dataframe(df) == [{"displayName": "John", "userPrincipalName": "jdoe@contoso.com"}]


def test_flat_round_trip():
    client = GraphClient()
    col = pandas__collection(
        [
            {"userPrincipalName": "jdoe@contoso.com", "displayName": "John Doe", "accountEnabled": True},
        ],
        context=client,
    )
    col.query_options.select = ["userPrincipalName", "displayName", "accountEnabled"]

    target = DataFrameResult(client)
    write_dataframe(col, target)

    imported = ClientObjectCollection(client, User, None)
    imported.from_dataframe(target.value)
    assert len(imported) == 1
    item = imported[0]
    assert item.get_property("userPrincipalName") == "jdoe@contoso.com"
    assert item.get_property("accountEnabled") is True


def test_to_dataframe_returns_dataframe_result():
    client = GraphClient()
    col = pandas__collection([{"displayName": "John Doe"}], context=client)
    result = col.to_dataframe()
    assert isinstance(result, DataFrameResult)
    # the after_execute callback materializes .value on the loaded collection
    write_dataframe(col, result)
    assert list(result.value.columns) == ["displayName"]


def test_records_from_dataframe_drops_nan_cells():
    df = pd.DataFrame({"a": [1.0, float("nan")], "b": ["x", "y"]})
    assert records_from_dataframe(df) == [{"a": 1.0, "b": "x"}, {"b": "y"}]


def test_field_type_mapping():
    assert field_type_from_kind(series_kind(pd, pd.Series([True]))) is FieldType.Boolean
    assert field_type_from_kind(series_kind(pd, pd.Series(pd.to_datetime(["2025-01-01"])))) is FieldType.DateTime
    assert field_type_from_kind(series_kind(pd, pd.Series([1.5]))) is FieldType.Number
    assert field_type_from_kind(series_kind(pd, pd.Series(["text"]))) is FieldType.Text
