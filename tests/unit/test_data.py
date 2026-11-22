"""The record pipeline: a table in, typed records queued, records out.

A record is a row of the *model*, so the columns a projection carries are the ones the
serializer and ``$select`` already agree on. Reading the response instead answered a
different question -- the keys one page happened to carry, sorted -- so an item with an
extra field reordered every header, and a declared column the service left out of a page
vanished rather than arriving empty.

The two files this replaces were the two directions of that same seam. One turned CSV, Excel
and a DataFrame into records and records back into a file; the other drove a table *into* a
model -- chunks, a checkpoint, a resume, a dead letter -- so a million rows survive a process
that dies at row 900,000. Neither direction is useful alone: the columns an export writes are
the columns an import parses, and both read them from the declaration.

The last heading is the async form of the same driver, not a second one. It is the only place
offline tests await a coroutine, because a chunked import is where writing the second
implementation would have been cheapest and where it actually exists.
"""

from __future__ import annotations

import asyncio
import io
import json
import unittest
import unittest.mock
import warnings
from datetime import datetime, timezone
from typing import Any, cast

import pytest
from office365.directory.users.user import User
from office365.graph_client import GraphClient
from office365.migration.offline import offline_context, offline_sharepoint_context
from office365.outlook.mail.messages.message import Message
from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.converters.csv_reader import read_csv_records
from office365.runtime.converters.csv_writer import write_records
from office365.runtime.converters.dataframe import (
    DataFrameResult,
    dataframe_chunks,
    series_kind,
    write_dataframe,
)
from office365.runtime.converters.excel import read_excel, write_excel
from office365.runtime.converters.records import declared_columns, deserialize_records, iter_records
from office365.runtime.converters.streamers import streamer_for
from office365.runtime.converters.upsert import keyed_queue, record_key
from office365.runtime.imports import ImportCheckpoint, ImportResult
from office365.runtime.operations import query_progress_hook
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.record_collection import RecordCollection
from office365.runtime.schema import TypeSchema
from office365.sharepoint.fields.collection import field_type_from_kind
from office365.sharepoint.fields.type import FieldType
from office365.sharepoint.folders.folder import Folder
from office365.sharepoint.listitems.collection import ListItemCollection

pd = pytest.importorskip("pandas")


CSV_TEXT = (
    "userPrincipalName,givenName,displayName,accountEnabled,officeLocation,"
    "passwordProfile/password,passwordProfile/forceChangePasswordNextSignIn,businessPhones\n"
    "jdoe@contoso.com,John,John Doe,True,Seattle,S3cret!,True,+1-555-0101; +1-555-0102\n"
)


# --- a table becomes records ----------------------------------------------------------


class TestCsvRecords(unittest.TestCase):
    def test_deserialize_records(self):
        records = deserialize_records(
            User,
            read_csv_records(io.StringIO(CSV_TEXT)),
        )
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record["userPrincipalName"], "jdoe@contoso.com")
        self.assertEqual(record["passwordProfile"], {"password": "S3cret!", "forceChangePasswordNextSignIn": "True"})
        self.assertEqual(record["businessPhones"], ["+1-555-0101", "+1-555-0102"])

    def test_deserialize_records_strips_non_importable_and_unknown(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            records = deserialize_records(
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
        client = GraphClient()  # never sent: these tests only queue records
        users = next(iter(client.users.from_csv(io.StringIO(CSV_TEXT))))
        self.assertEqual(len(users), 1)
        self.assertEqual(len(client._queries), 1)
        user = users[0]
        self.assertIs(user.get_property("accountEnabled"), True)
        self.assertEqual(user.get_property("passwordProfile").password, "S3cret!")
        self.assertIs(user.get_property("passwordProfile").forceChangePasswordNextSignIn, True)
        self.assertEqual(list(user.get_property("businessPhones")), ["+1-555-0101", "+1-555-0102"])

    def test_round_trip_write_then_read(self):
        col = RecordCollection(offline_context(), User, None)
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
        write_records(iter_records(col), out)

        client = GraphClient()  # never sent: these tests only queue records
        users = next(iter(client.users.from_csv(io.StringIO(out.getvalue()))))
        user = users[0]
        self.assertIs(user.get_property("accountEnabled"), True)
        self.assertEqual(user.get_property("createdDateTime"), datetime(2025, 1, 15, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(list(user.get_property("businessPhones")), ["+1-555-0101", "+1-555-0102"])


# --- what a record knows about its columns --------------------------------------------


def test_list_item_collection_from_records_keeps_custom_columns():
    col = ListItemCollection(offline_context())
    col.queue_records([{"Title": "row", "CustomColumn": 42}])

    assert len(col) == 1
    assert col[0].get_property("CustomColumn") == 42  # noqa: PLR2004
    assert col[0].get_property("Title") == "row"


openpyxl = pytest.importorskip("openpyxl")


def _users(properties: list[dict], context=None) -> RecordCollection:
    col = RecordCollection(context or offline_context(), User, None)
    for props in properties:
        col.add_child(col.create_typed_object(props))
    return col


def test_excel_round_trip(tmp_path):
    records = [{"Name": "John", "Age": 30}, {"Name": "Alice", "Age": 25}]
    path = str(tmp_path / "out.xlsx")
    write_excel(records, path)
    assert read_excel(path) == records


def test_query_progress_hook():
    events = []
    hook = query_progress_hook(3, events.append, stage="importing")
    for _ in range(3):
        hook(None)  # each call mimics one queued query completing
    assert [p.done for p in events] == [1, 2, 3]  # noqa: PLR2004
    assert all(p.total == 3 for p in events)  # noqa: PLR2004
    assert all(p.stage == "importing" for p in events)
    assert events[-1].percent == 100.0  # noqa: PLR2004


pd = pytest.importorskip("pandas")


def test_flat_round_trip():
    client = GraphClient()
    col = _users(
        [
            {"userPrincipalName": "jdoe@contoso.com", "displayName": "John Doe", "accountEnabled": True},
        ],
        context=client,
    )
    col.query_options.select = ["userPrincipalName", "displayName", "accountEnabled"]

    target = DataFrameResult(client)
    write_dataframe(col, target)

    imported = RecordCollection(client, User, None)
    imported.queue_dataframe(target.value)
    assert len(imported) == 1
    item = imported[0]
    assert item.get_property("userPrincipalName") == "jdoe@contoso.com"
    assert item.get_property("accountEnabled") is True


def test_to_dataframe_returns_dataframe_result():
    client = GraphClient()
    col = _users([{"displayName": "John Doe", "contosoExtension": "x"}], context=client)
    result = col.to_dataframe()
    assert isinstance(result, DataFrameResult)
    # the after_execute callback materializes .value on the loaded collection
    write_dataframe(col, result)
    # The columns are the type's, in declaration order, then the name only this page
    # carried: a row is a row of the model, not of the response. ``displayName`` is a
    # column of the model now, so the page-only name has to be one the model cannot
    # spell.
    assert list(result.value.columns) == [*TypeSchema.of(User).columns, "contosoExtension"]
    assert result.value["displayName"].tolist() == ["John Doe"]


def test_field_type_mapping():
    assert field_type_from_kind(series_kind(pd, pd.Series([True]))) is FieldType.Boolean
    assert field_type_from_kind(series_kind(pd, pd.Series(pd.to_datetime(["2025-01-01"])))) is FieldType.DateTime
    assert field_type_from_kind(series_kind(pd, pd.Series([1.5]))) is FieldType.Number
    assert field_type_from_kind(series_kind(pd, pd.Series(["text"]))) is FieldType.Text


def test_internal_field_name_sanitizes_and_avoids_reserved_titles():
    from office365.sharepoint.fields.name import internal_field_name, is_reserved_field_title

    assert internal_field_name("My Column") == "My_Column"
    assert internal_field_name("Symbol") == "Symbol"
    # reserved built-in display names are suffixed so the column can be created
    assert internal_field_name("Name") == "Name_"
    assert internal_field_name("Title") == "Title_"
    assert is_reserved_field_title("name")
    assert not is_reserved_field_title("Symbol")


class _Client:
    """A client that addresses one version, as ``GraphClient`` does."""

    version = "v1.0"


def _collection(properties: list[dict], item_type: type = User, context: Any = None) -> ClientObjectCollection:
    col = ClientObjectCollection(context, item_type, None)
    for props in properties:
        col.add_child(col.create_typed_object(props))
    return col


def test_headers_are_the_declared_columns_even_when_the_page_omits_them() -> None:
    columns = TypeSchema.of(User).columns
    page = _collection([{columns[0]: "a value"}])
    record = iter_records(page)[0]

    assert list(record) == list(columns), "declaration order, and every column present"
    assert record[columns[0]] == "a value"
    assert record[columns[1]] is None, "a column the page omitted is empty, not missing"
    # And the projection of the page is what the reader was handed: one answer, asked twice.
    assert declared_columns(list(page)) == list(record)


def test_a_name_the_metadata_does_not_describe_still_follows() -> None:
    """The whole defect: one page's extra column used to move every header.

    A site column, or a property the CSDL has no member for, exists on the wire and has to
    survive the round trip -- after the declared ones, and in the same place on every row.
    """
    columns = TypeSchema.of(User).columns
    records = iter_records(_collection([{columns[0]: "a"}, {columns[0]: "b", "siteColumn": "kept"}]))

    for record in records:
        assert list(record)[: len(columns)] == list(columns)
        assert list(record) == [*columns, "siteColumn"]
    assert records[0]["siteColumn"] is None  # a column of the page, empty on the row without it


def test_an_explicit_select_is_the_export() -> None:
    col = _collection([{"displayName": "John", "accountEnabled": True, "ignored": 1}])
    col.query_options.select = ["displayName", "accountEnabled"]

    assert list(iter_records(col)[0]) == ["displayName", "accountEnabled"]


def test_the_projection_speaks_the_clients_version() -> None:
    """A stable client exports no preview column, even one this page carried."""
    beta_columns = Message._schema.beta_only
    page = [{"id": "1", "unsubscribeEnabled": True}]
    stable = iter_records(_collection(page, Message, _Client()))[0]

    assert beta_columns, "the fixture must carry preview-only members to prove anything"
    assert not beta_columns & set(stable)
    assert list(stable) == [name for name in TypeSchema.of(Message).columns if name not in beta_columns]


def test_rows_from_makes_one_record_per_child_of_a_complex_collection() -> None:
    """A licence is a child, not a cell — and Graph will not project one.

    ``$expand=assignedLicenses`` is refused ("not a navigation property or complex
    property") and ``$select=assignedLicenses/skuId`` is refused ("invalid property"),
    so the child's own properties have to become the columns.
    """
    page = _collection(
        [
            {
                "userPrincipalName": "a@example.com",
                "assignedLicenses": [
                    {"skuId": "sku-1", "disabledPlans": ["plan-1"]},
                    {"skuId": "sku-2", "disabledPlans": ["plan-2"]},
                ],
            }
        ]
    )
    page.query_options.select = ["userPrincipalName", "assignedLicenses"]

    assert iter_records(page, rows_from="assignedLicenses") == [
        {"userPrincipalName": "a@example.com", "skuId": "sku-1", "disabledPlans": ["plan-1"]},
        {"userPrincipalName": "a@example.com", "skuId": "sku-2", "disabledPlans": ["plan-2"]},
    ]


def test_rows_from_needs_a_column_that_says_whose_row_it_is() -> None:
    """Fanning out over the only selected column would write rows nobody can attribute."""
    page = _collection([{"assignedLicenses": [{"skuId": "sku-1"}]}])
    page.query_options.select = ["assignedLicenses"]

    with pytest.raises(ValueError, match="whose row"):
        iter_records(page, rows_from="assignedLicenses")


# --- a record becomes a write ---------------------------------------------------------


# Key-based, idempotent record imports (skip / update).
class _FakeTarget:
    """Minimal UpsertTarget capturing what gets queued."""

    def __init__(self, key_field: str = "MigrationKey") -> None:
        self._key_field = key_field
        self.created: list[dict] = []
        self.updated: list[tuple[int, dict]] = []

    @property
    def key_field(self) -> str:
        return self._key_field

    def ensure_key_field(self) -> None: ...

    def load_keys(self):
        return {}

    def create_records(self, records):
        self.created.extend(records)

    def update_record(self, item_id, record):
        self.updated.append((item_id, record))


def _queue(target, records, existing, *, on_conflict="skip", dry_run=False):
    return keyed_queue(
        target,
        records,
        key_columns=["Name_", "date"],
        existing=existing,
        on_conflict=on_conflict,
        dry_run=dry_run,
    )


def test_record_key_is_deterministic_and_key_sensitive():
    columns = ["Name_", "date"]
    a = record_key({"Name_": "AAPL", "date": "2013-02-08"}, columns)
    b = record_key({"date": "2013-02-08", "Name_": "AAPL"}, columns)
    c = record_key({"Name_": "MSFT", "date": "2013-02-08"}, columns)

    assert a == b  # record key order doesn't matter
    assert a != c  # different values -> different key
    assert len(a) == 64  # noqa: PLR2004 — sha-256 hex


def test_keyed_queue_skips_existing():
    target = _FakeTarget()
    records = [{"Name_": "AAPL", "date": "d1"}, {"Name_": "AAPL", "date": "d2"}]
    existing = {record_key(records[0], ["Name_", "date"]): 1}

    queued, skipped = _queue(target, records, existing)

    assert (queued, skipped) == (1, 1)
    assert len(target.created) == 1  # only the new row
    assert target.updated == []
    assert records[1]["MigrationKey"] == record_key(records[1], ["Name_", "date"])


def test_keyed_queue_upserts_existing():
    target = _FakeTarget()
    records = [{"Name_": "AAPL", "date": "d1"}, {"Name_": "AAPL", "date": "d2"}]
    existing = {record_key(records[0], ["Name_", "date"]): 7}

    queued, skipped = _queue(target, records, existing, on_conflict="update")

    assert (queued, skipped) == (2, 0)
    assert len(target.created) == 1  # the new row
    assert target.updated[0][0] == 7  # noqa: PLR2004 — the existing row id


# --- an export -----------------------------------------------------------------------


def _rows(path) -> list:
    """What a reader sees in a file a writer just closed."""
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return read_csv_records(handle)


def _resolved_users(*names: str) -> RecordCollection:
    """A collection already resolved: nothing is pending, nothing will be fetched."""
    col = RecordCollection(GraphClient(), User, None)
    for name in names:
        col.add_child(col.create_typed_object({"userPrincipalName": f"{name}@contoso.com", "displayName": name}))
    col.query_options.select = ["userPrincipalName", "displayName"]
    return col


def test_a_resolved_collection_exports_without_a_second_round_trip(tmp_path):
    # ``execute_query(); to_csv(path)`` is what a chained read leaves behind: an export
    # registered through ``after_execute`` would never fire, because nothing is pending.
    path = tmp_path / "loaded.csv"

    _resolved_users("A", "B").to_csv(str(path))

    assert [r["displayName"] for r in _rows(path)] == ["A", "B"]


def test_a_paged_export_writes_the_header_once(tmp_path):
    # One writer per page, so the header belongs to the first one: a page loop that reopened
    # the file per page would repeat it, and a reader would see the header as a row.
    path = tmp_path / "paged.csv"
    factory = streamer_for("csv")
    assert factory is not None, "csv is appendable, so a paged export exists"
    stream = factory(str(path))
    stream.write([{"a": 1, "b": "x"}])
    stream.write([{"a": 2, "b": "y"}])
    stream.close()

    assert path.read_text(encoding="utf-8").count("a,b") == 1
    assert [r["a"] for r in _rows(path)] == ["1", "2"]


def test_a_dataframe_uploaded_to_a_folder_is_utf8_with_a_bom():
    pd = pytest.importorskip("pandas")
    folder = Folder(offline_sharepoint_context(), ResourcePath("Web/getFolderByServerRelativeUrl('Shared Documents')"))

    with unittest.mock.patch.object(Folder, "upload_file") as upload:
        folder.write_dataframe("data.csv", pd.DataFrame({"a": [1, 2]}))

    name, content = upload.call_args.args[:2]
    assert name == "data.csv"
    assert content.startswith(b"\xef\xbb\xbf")  # utf-8-sig, so Excel keeps the columns as columns


class _FakeCollection:
    def __init__(self) -> None:
        self.queued: list[dict] = []
        self.clears = 0

    def queue_records(self, records, progress=None):
        self.queued.extend(records)
        return self

    def clear(self):
        self.clears += 1
        return self


class _FakeContext:
    def __init__(self) -> None:
        self.query_calls = 0
        self.batch_calls: list[dict] = []

    def execute_query(self):
        self.query_calls += 1
        return self

    def execute_batch(self, items_per_batch=100, max_batch_bytes=None, concurrency=1, success_callback=None):
        self.batch_calls.append({"items_per_batch": items_per_batch, "concurrency": concurrency})
        return self


class _FlakyContext(_FakeContext):
    def __init__(self, fail_on: int) -> None:
        super().__init__()
        self._fail_on = fail_on
        self.calls = 0

    def execute_query(self):
        self.calls += 1
        if self.calls == self._fail_on:
            raise RuntimeError("boom")
        return super().execute_query()


class _AsyncFakeContext(_FakeContext):
    """Async terminals mirroring ``_FakeContext`` (must be awaited)."""

    async def execute_query_async(self):
        self.query_calls += 1
        return self

    async def execute_batch_async(self, items_per_batch=100, max_batch_bytes=None, concurrency=1, success_callback=None):
        self.batch_calls.append({"items_per_batch": items_per_batch, "concurrency": concurrency})
        return self


class _AsyncFlakyContext(_AsyncFakeContext):
    def __init__(self, fail_on: int) -> None:
        super().__init__()
        self._fail_on = fail_on
        self.calls = 0

    async def execute_query_async(self):
        self.calls += 1
        if self.calls == self._fail_on:
            raise RuntimeError("boom")
        return await super().execute_query_async()


def _batches(*sizes: int) -> list[list[dict]]:
    out: list[list[dict]] = []
    n = 0
    for size in sizes:
        out.append([{"n": n + i} for i in range(size)])
        n += size
    return out


def _driver(context, collection, batches, **kwargs) -> ImportResult:
    return ImportResult(context, collection, batches, map=lambda b: b, **kwargs)


# --- the import driver ----------------------------------------------------------------


def test_execute_query_chunks_once_and_bounds_memory():
    ctx = _FakeContext()
    collection = _FakeCollection()
    driver = _driver(ctx, collection, _batches(2, 2, 1))

    driver.execute_query()

    assert collection.clears == 3  # noqa: PLR2004 — one clear per chunk
    assert driver.value.total == 5  # noqa: PLR2004
    assert driver.value.success == 5  # noqa: PLR2004
    assert driver.value.chunks == 3  # noqa: PLR2004
    assert ctx.query_calls == 3  # noqa: PLR2004
    assert len(collection.queued) == 5  # noqa: PLR2004


def test_dry_run_plans_without_queueing_or_executing():
    ctx = _FakeContext()
    collection = _FakeCollection()
    driver = _driver(ctx, collection, _batches(2, 2), dry_run=True)

    driver.execute_query()

    assert ctx.query_calls == 0  # nothing executed
    assert collection.queued == []  # nothing queued
    assert driver.value.total == 4  # noqa: PLR2004 — plan counted
    assert driver.value.success == 4  # noqa: PLR2004


def test_iter_yields_the_collection_and_drives_execution():
    ctx = _FakeContext()
    collection = _FakeCollection()
    driver = _driver(ctx, collection, _batches(1, 1, 1))

    for yielded in driver:
        assert yielded is collection
        ctx.execute_query()

    assert driver.value.total == 3  # noqa: PLR2004
    assert collection.clears == 3  # noqa: PLR2004


def test_checkpoint_round_trips(tmp_path):
    path = tmp_path / "ckpt.json"
    ImportCheckpoint(cursor=10, chunks=2, errors=1, failures=[{"records": 1, "error": "x"}]).save(path)

    loaded = ImportCheckpoint.load(path)

    assert loaded.cursor == 10  # noqa: PLR2004
    assert loaded.chunks == 2  # noqa: PLR2004
    assert loaded.errors == 1
    assert loaded.failures == [{"records": 1, "error": "x"}]


def test_resume_skips_committed_records(tmp_path):
    path = tmp_path / "ckpt.json"

    # first run commits the first two chunks (4 records)
    _driver(_FakeContext(), _FakeCollection(), _batches(2, 2), checkpoint=str(path)).execute_query()
    assert ImportCheckpoint.load(path).cursor == 4  # noqa: PLR2004

    # a resumed run (fresh source) skips the committed records
    collection = _FakeCollection()
    driver = _driver(_FakeContext(), collection, _batches(2, 2, 2), checkpoint=str(path))
    driver.execute_query()

    assert collection.queued == [{"n": 4}, {"n": 5}]
    assert driver.value.total == 2  # noqa: PLR2004
    assert driver.value.success == 2  # noqa: PLR2004


def test_resume_accessors_and_summary(tmp_path):
    path = tmp_path / "ckpt.json"
    _driver(_FakeContext(), _FakeCollection(), _batches(2, 2), checkpoint=str(path)).execute_query()

    driver = _driver(_FakeContext(), _FakeCollection(), _batches(2, 2, 2), checkpoint=str(path))
    assert driver.resumed_from == 4  # noqa: PLR2004
    assert driver.value.resumed_from == 4  # noqa: PLR2004
    assert driver.checkpoint.cursor == 4  # noqa: PLR2004

    driver.execute_query()

    assert driver.checkpoint.cursor == 6  # noqa: PLR2004
    assert "resumed at 4" in driver.value.summary()


def test_custom_checkpoint_store(tmp_path):
    from office365.runtime.imports import FileCheckpointStore, MemoryCheckpointStore

    store = MemoryCheckpointStore(ImportCheckpoint(cursor=2, chunks=1))
    driver = _driver(_FakeContext(), _FakeCollection(), _batches(2, 2), checkpoint=store)
    assert driver.resumed_from == 2  # noqa: PLR2004

    driver.execute_query()
    assert store.load().cursor == 4  # noqa: PLR2004

    file_store = FileCheckpointStore(tmp_path / "c.json")
    assert file_store.load().cursor == 0
    file_store.save(ImportCheckpoint(cursor=7))
    assert file_store.load().cursor == 7  # noqa: PLR2004


def test_on_error_collect_records_and_continues():
    ctx = _FlakyContext(fail_on=2)
    collection = _FakeCollection()
    checkpoint = ImportCheckpoint()
    driver = _driver(ctx, collection, _batches(2, 2, 2), checkpoint=checkpoint, on_error="collect")

    driver.execute_query()

    assert driver.value.total == 6  # noqa: PLR2004
    assert driver.value.success == 4  # noqa: PLR2004
    assert driver.value.errors == 2  # noqa: PLR2004
    assert len(checkpoint.failures) == 1
    assert checkpoint.failures[0]["records"] == 2  # noqa: PLR2004
    assert checkpoint.cursor == 6  # noqa: PLR2004 — failed chunk is skipped, not retried


def test_execute_batch_reports_progress_per_batch_and_forwards_callback():
    class _BatchingContext(_FakeContext):
        def execute_batch(self, items_per_batch=100, max_batch_bytes=None, concurrency=1, success_callback=None):
            for _ in range(2):  # two sub-batches of two items each
                if callable(success_callback):
                    success_callback([1, 2])
            return self

    seen: list[Any] = []
    forwarded: list[Any] = []
    driver = _driver(_BatchingContext(), _FakeCollection(), _batches(4), progress=seen.append, total=4)

    driver.execute_batch(items_per_batch=2, success_callback=forwarded.append)

    assert [p.done for p in seen] == [0, 2, 4]
    assert len(forwarded) == 2  # noqa: PLR2004


def test_dead_letter_isolates_the_failed_record(tmp_path):
    path = tmp_path / "dl.jsonl"
    ctx = _FlakyContext(fail_on=2)
    collection = _FakeCollection()
    driver = _driver(ctx, collection, _batches(2, 2, 2), on_error="collect", dead_letter=str(path))

    driver.execute_query()

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1  # only the failing row is dead-lettered
    entry = json.loads(lines[0])
    assert entry["row"] == 1
    assert entry["record"] == {"n": 1}
    assert entry["error"] == "boom"


def test_dataframe_chunks_reads_csv(tmp_path):
    path = tmp_path / "rows.csv"
    path.write_text("n\na\nb\nc\n", encoding="utf-8")
    chunks, total = dataframe_chunks(str(path), chunksize=1)

    assert total is None
    assert len(list(chunks)) == 3  # noqa: PLR2004


def test_list_from_dataframe_returns_import_result():
    from office365.sharepoint.lists.list import List

    ctx = _FakeContext()
    lst = List(cast(Any, ctx))
    driver = lst.from_dataframe(pd.DataFrame({"Name": ["a"], "Value": [1]}))

    assert isinstance(driver, ImportResult)


class _KeyedTarget:
    def __init__(self, keys: list[str]) -> None:
        self._keys = keys

    def load_keys(self):
        return {key: index for index, key in enumerate(self._keys)}


class _KeyedCollection(_FakeCollection):
    def __init__(self, keys: list[str]) -> None:
        super().__init__()
        self._keys = keys

    def upsert_target(self, *, key_field: str = "MigrationKey", enforce_unique: bool = False):
        return _KeyedTarget(self._keys)


# --- a keyed target, and what it verifies ---------------------------------------------


def test_from_records_applies_column_mapping():
    from office365.runtime.client_object import ClientObject
    from office365.runtime.record_collection import RecordCollection

    class _RecordFake(RecordCollection):
        def __init__(self, context):
            super().__init__(context, ClientObject)
            self.queued = []

        def queue_records(self, records, progress=None):
            self.queued.extend(records)
            return self

    collection = _RecordFake(cast(Any, _FakeContext()))
    result = RecordCollection.from_records(
        collection,
        _batches(1),
        format="records",
        map=lambda records: [{"value": record["n"]} for record in records],
    )

    result.execute_query()

    assert collection.queued == [{"value": 0}]


def test_verify_keys_reports_missing():
    from office365.runtime.record_collection import RecordCollection, VerificationResult

    result = RecordCollection.verify_keys(cast(Any, _KeyedCollection(["a", "b"])), ["a", "b", "c"])

    assert isinstance(result, VerificationResult)
    assert result.checked == 3  # noqa: PLR2004
    assert result.source_count == 3  # noqa: PLR2004
    assert result.target_count == 2  # noqa: PLR2004
    assert result.missing == ["c"]
    assert not result.ok
    assert "MISMATCH" in result.summary()


def test_import_result_run_is_the_batch_terminal():
    ctx = _FakeContext()
    driver = _driver(ctx, _FakeCollection(), _batches(2, 2))

    driver.run(items_per_batch=2, concurrency=3)

    assert len(ctx.batch_calls) == 2  # noqa: PLR2004 — one batch call per chunk
    assert all(call == {"items_per_batch": 2, "concurrency": 3} for call in ctx.batch_calls)


def test_collection_verify_reconciles_source_keys():
    from office365.runtime.converters.upsert import record_key
    from office365.runtime.record_collection import RecordCollection

    existing = {record_key({"id": 1}, ["id"]): 11}
    collection = _ImportCollection(existing=existing)

    report = RecordCollection.verify(collection, [[{"id": 1}, {"id": 2}]], key=["id"], format="records")

    assert report.source_count == 2  # noqa: PLR2004
    assert report.target_count == 1
    assert report.missing == [record_key({"id": 2}, ["id"])]
    assert not report.ok


def test_import_result_verify_delegates_to_collection():
    from office365.runtime.converters.upsert import record_key
    from office365.runtime.imports import ImportResult

    existing = {record_key({"id": 1}, ["id"]): 11}
    collection = _ImportCollection(existing=existing)
    driver = ImportResult(
        cast(Any, collection.context),
        collection,
        [[{"id": 1}, {"id": 2}]],
        map=lambda batch: batch,
    )

    report = driver.verify([[{"id": 1}, {"id": 2}]], key=["id"], format="records")

    assert report.missing == [record_key({"id": 2}, ["id"])]


# --- resuming against a real collection -----------------------------------------------


class _ImportTarget:
    """Fake keyed target recording the key-load/ensure calls."""

    def __init__(self, collection: "_ImportCollection", key_field: str) -> None:
        self._collection = collection
        self._key_field = key_field

    @property
    def key_field(self) -> str:
        return self._key_field

    def ensure_key_field(self) -> None:
        self._collection.ensured += 1

    def load_keys(self):
        self._collection.load_calls += 1
        return dict(self._collection.existing)

    def create_records(self, records: list[dict]) -> None:
        self._collection.created.extend(records)

    def update_record(self, item_id, record: dict) -> None:
        self._collection.updated.append((item_id, record))


class _ImportCollection(RecordCollection):
    """Fake record collection driving the real ``RecordCollection.from_records``."""

    def __init__(self, existing: dict | None = None, item_type: type = ClientObject) -> None:
        super().__init__(cast(Any, _FakeContext()), item_type)
        self.existing = dict(existing or {})
        self.created: list[dict] = []
        self.updated: list = []
        self.load_calls = 0
        self.ensured = 0

    def queue_records(self, records, progress=None):
        self.created.extend(records)
        return self

    def upsert_target(self, *, key_field: str = "MigrationKey", enforce_unique: bool = False):
        return _ImportTarget(self, key_field)


def test_resume_loads_existing_keys_and_skips_duplicates():
    from office365.runtime.converters.upsert import record_key
    from office365.runtime.imports import ImportCheckpoint
    from office365.runtime.record_collection import RecordCollection

    existing = {record_key({"id": 1}, ["id"]): 11}
    collection = _ImportCollection(existing=existing)
    checkpoint = ImportCheckpoint(cursor=1, chunks=1)  # skip the first batch

    driver = RecordCollection.from_records(
        collection,
        [[{"id": 0}], [{"id": 1}], [{"id": 2}]],
        format="records",
        key=["id"],
        checkpoint=checkpoint,
    )
    driver.execute_query()

    assert collection.load_calls == 1  # keys are loaded on a resumed run too
    assert collection.ensured == 1
    assert [record["id"] for record in collection.created] == [2]  # id=1 skipped by key
    assert collection.created[0]["MigrationKey"] == record_key({"id": 2}, ["id"])


def test_checkpoint_signature_mismatch_rescans_from_start():
    from office365.runtime.imports import ImportCheckpoint
    from office365.runtime.record_collection import RecordCollection

    checkpoint = ImportCheckpoint(cursor=1, chunks=1, signature={"format": "records", "chunk_size": 2000})
    collection = _ImportCollection()

    with pytest.warns(UserWarning, match="signature changed"):
        driver = RecordCollection.from_records(
            collection,
            [[{"id": 0}], [{"id": 1}]],
            format="records",
            chunksize=1000,  # differs from the stored signature
            key=["id"],
            checkpoint=checkpoint,
        )

    assert driver.resumed_from == 0  # chunk skip discarded
    driver.execute_query()
    assert [record["id"] for record in collection.created] == [0, 1]  # re-scanned


# --- a converter declared per column --------------------------------------------------


def test_from_records_applies_converters():
    """A converter wins over the declared property type, and runs exactly once."""
    from office365.directory.users.user import User
    from office365.runtime.record_collection import RecordCollection

    collection = _ImportCollection(item_type=User)
    driver = RecordCollection.from_records(
        collection,
        [[{"displayName": "ann"}]],
        format="records",
        converters={"displayName": lambda value: value.upper()},
    )
    driver.execute_query()

    assert collection.created == [{"displayName": "ANN"}]


def test_a_converter_for_an_undeclared_column_raises():
    """A misspelt destination key must not silently mean "the column was dropped"."""
    from office365.runtime.record_collection import RecordCollection

    collection = _ImportCollection()
    with pytest.raises(ValueError, match="no column 'n'"):
        RecordCollection.from_records(
            collection,
            [[{"n": "2"}]],
            format="records",
            converters={"n": int},
        )


def test_a_target_that_accepts_unknown_columns_keeps_the_coercion():
    """A list item forwards every key, so its columns are known only at runtime."""
    from office365.runtime.record_collection import RecordCollection

    collection = _ImportCollection()
    collection._accepts_unknown_columns = True
    driver = RecordCollection.from_records(
        collection,
        [[{"n": "30"}]],
        format="records",
        converters={"n": "Edm.Int32"},
    )
    driver.execute_query()

    assert collection.created == [{"n": 30}]


# --- the same driver, awaited ---------------------------------------------------------


def test_import_result_run_async_is_the_batch_terminal():
    ctx = _AsyncFakeContext()
    driver = _driver(ctx, _FakeCollection(), _batches(2, 2))

    asyncio.run(driver.run_async(items_per_batch=2, concurrency=3))

    assert len(ctx.batch_calls) == 2  # noqa: PLR2004 — one batch call per chunk
    assert all(call == {"items_per_batch": 2, "concurrency": 3} for call in ctx.batch_calls)


def test_on_error_raise_async_aborts():
    ctx = _AsyncFlakyContext(fail_on=2)
    collection = _FakeCollection()
    driver = _driver(ctx, collection, _batches(2, 2, 2))

    with pytest.raises(RuntimeError):
        asyncio.run(driver.execute_query_async())

    assert driver.value.success == 2  # noqa: PLR2004
    assert driver.value.errors == 2  # noqa: PLR2004


def test_aiter_yields_the_collection_and_drives_execution():
    ctx = _AsyncFakeContext()
    collection = _FakeCollection()
    driver = _driver(ctx, collection, _batches(1, 1, 1))

    async def _consume():
        async for yielded in driver:
            assert yielded is collection
            await ctx.execute_query_async()

    asyncio.run(_consume())

    assert driver.value.total == 3  # noqa: PLR2004
    assert collection.clears == 3  # noqa: PLR2004
    assert ctx.query_calls == 3  # noqa: PLR2004
