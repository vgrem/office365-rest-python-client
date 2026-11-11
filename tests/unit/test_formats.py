"""Both ends of the pipeline: the format table, and the file bridge that feeds it.

A collection leaves as any format the registry knows - synchronously, page by page, or through a
stream that is closed even when the next page fails - and it arrives from a spreadsheet that lives
in SharePoint. The optional dependencies are skipped, not faked: a format that is not installed is
a format nobody can be wrong about.
"""

from __future__ import annotations

import asyncio
import io
import json
from unittest import mock

import pytest
from office365.directory.users.user import User
from office365.migration.offline import offline_sharepoint_context
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.converters import registry
from office365.runtime.converters.dataframe import dataframe_from_bytes, dataframe_to_bytes
from office365.runtime.converters.streamers import streamer_for
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.record_collection import RecordCollection
from office365.sharepoint.folders.folder import Folder
from office365.sharepoint.lists.list import List
from tests._scripted_transport import graph, sharepoint

pd = pytest.importorskip("pandas")

RECORDS = [
    {"userPrincipalName": "a@contoso.com", "displayName": "A", "accountEnabled": True},
    {"userPrincipalName": "b@contoso.com", "displayName": "B", "accountEnabled": False},
]

_GRAPH_NEXT = "https://graph.microsoft.com/v1.0/users?$skiptoken=abc"


def _collection(records=RECORDS) -> RecordCollection:
    col = RecordCollection(graph()[0], User, None)
    for props in records:
        col.add_child(col.create_typed_object(props))
    col.query_options.select = list(records[0].keys())
    return col


def _list(payloads) -> List:
    """A SharePoint list whose items answer from ``payloads``, in call order."""
    ctx = sharepoint(payloads)[0]
    lst = List(ctx, ResourcePath("Web/Lists/getByTitle('Tasks')"))
    # ``List.items`` builds a fresh collection on each access; pin one instance.
    lst.properties["Items"] = lst.items
    return lst


def _sp_page(records) -> dict:
    return {"d": {"results": records}}


def _read(fmt: str, path) -> list:
    return registry.reader_for(fmt)(str(path))


@pytest.mark.parametrize("fmt", ["parquet", "orc", "feather"])
def test_pyarrow_formats_round_trip(tmp_path, fmt):
    pytest.importorskip("pyarrow")
    path = tmp_path / f"data.{fmt}"

    registry.writer_for(fmt)(_collection(), str(path))

    assert [r["displayName"] for r in _read(fmt, path)] == ["A", "B"]


def test_streaming_csv_writer_appends_pages(tmp_path):
    path = tmp_path / "out.csv"
    stream = streamer_for("csv")(str(path))
    stream.write([{"a": 1, "b": "x"}])
    stream.write([{"a": 2, "b": "y"}])
    stream.close()

    assert path.read_text(encoding="utf-8").count("a,b") == 1  # header written once
    assert [r["a"] for r in _read("csv", path)] == ["1", "2"]


def test_streaming_json_writer_appends_pages(tmp_path):
    path = tmp_path / "out.json"
    stream = streamer_for("json")(str(path))
    stream.write([{"a": 1}])
    stream.write([{"a": 2}])
    stream.close()

    assert json.loads(path.read_text(encoding="utf-8")) == [{"a": 1}, {"a": 2}]


def test_duckdb_reads_in_chunks_and_writes_a_table():
    duckdb = pytest.importorskip("duckdb")
    from office365.runtime.converters.sql import duckdb_chunks, write_duckdb

    con = duckdb.connect()
    con.execute("CREATE TABLE src AS SELECT 'A' AS displayName, 1 AS n")

    assert list(duckdb_chunks(con, "SELECT * FROM src", 1)) == [[{"displayName": "A", "n": 1}]]

    write_duckdb(RECORDS, con, table="dst")
    assert con.execute("SELECT count(*) FROM dst").fetchone()[0] == len(RECORDS)


def test_to_csv_writes_an_already_loaded_collection(tmp_path):
    """Export a resolved collection without a second ``execute_query()``.

    ``col.execute_query(); col.to_csv(path)`` is the shape a chained read (``after_execute``)
    leaves behind: nothing is pending, so a handler registered through ``after_execute`` would
    never fire.
    """
    path = tmp_path / "loaded.csv"

    _collection().to_csv(str(path))

    assert [r["userPrincipalName"] for r in _read("csv", path)] == ["a@contoso.com", "b@contoso.com"]


def test_export_to_streams_pages_sync(tmp_path):
    client, transport = graph(
        [
            {"@odata.nextLink": _GRAPH_NEXT, "value": [{"displayName": "A"}, {"displayName": "B"}]},
            {"value": [{"displayName": "C"}]},
        ]
    )
    path = tmp_path / "users_sync.csv"

    client.users.export_to(str(path), format="csv", page_size=2).execute_query()

    assert transport.calls == 2  # noqa: PLR2004
    assert [r["displayName"] for r in _read("csv", path)] == ["A", "B", "C"]


def test_export_to_async_closes_stream_on_failure(tmp_path):
    client, _ = graph([{"@odata.nextLink": _GRAPH_NEXT, "value": [{"id": "1"}]}, ("deny", None)])
    path = tmp_path / "partial.csv"

    with pytest.raises(ClientRequestException):
        asyncio.run(client.users.export_to_async(str(path), format="csv", page_size=1))

    # The first page was flushed and the writer closed despite the failure.
    assert [r["id"] for r in _read("csv", path)] == ["1"]


def test_list_export_to_async_streams_items(tmp_path):
    lst = _list([_sp_page([{"Title": "A"}]), _sp_page([{"Title": "B"}]), _sp_page([])])
    path = tmp_path / "items.csv"

    asyncio.run(lst.export_to_async(str(path), page_size=1))

    assert lst.context.pending_request().transport.calls == 3  # noqa: PLR2004
    assert [r["Title"] for r in _read("csv", path)] == ["A", "B"]


def test_list_export_to_async_writes_loaded_items(tmp_path):
    lst = _list([_sp_page([{"Title": "A"}, {"Title": "B"}])])
    path = tmp_path / "loaded.csv"

    asyncio.run(lst.export_to_async(str(path)))

    assert lst.context.pending_request().transport.calls == 1
    assert [r["Title"] for r in _read("csv", path)] == ["A", "B"]


def test_write_dataframe_writes_utf8_sig_bytes():
    folder = Folder(offline_sharepoint_context(), ResourcePath("Web/getFolderByServerRelativeUrl('Shared Documents')"))

    with mock.patch.object(Folder, "upload_file") as upload:
        folder.write_dataframe("data.csv", pd.DataFrame({"a": [1, 2]}))

    path, content = upload.call_args.args[:2]
    assert path == "data.csv"
    assert content.startswith(b"\xef\xbb\xbf")  # utf-8-sig BOM, so Excel keeps the columns
    assert b"a" in content and b"1" in content


def test_dataframe_bytes_round_trip_csv():
    back = dataframe_from_bytes(dataframe_to_bytes(pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})))

    assert list(back["a"]) == [1, 2]
    assert list(back["b"]) == ["x", "y"]


def test_from_file_downloads_and_streams_csv():
    csv = b"Name,date\nAAPL,2020-01-01\n"
    lst = _list([csv])

    with mock.patch.object(List, "from_records", return_value="driver") as from_records:
        assert lst.from_file("Shared Documents/stocks.csv", key=["Name", "date"]) == "driver"

    source = from_records.call_args.args[0]
    assert isinstance(source, io.BytesIO)
    assert source.getvalue() == csv
    assert from_records.call_args.kwargs == {"format": "csv", "chunksize": 2000, "key": ["Name", "date"]}


def test_from_file_reads_xlsx_into_dataframe():
    pytest.importorskip("openpyxl")
    buffer = io.BytesIO()
    pd.DataFrame({"a": [1]}).to_excel(buffer, index=False)
    lst = _list([buffer.getvalue()])

    with mock.patch.object(List, "from_records", return_value="driver") as from_records:
        lst.from_file("Shared Documents/stocks.xlsx", format="xlsx")

    # A worksheet is a DataFrame before it is records: ``from_dataframe`` does the splitting.
    assert isinstance(from_records.call_args.args[0], pd.DataFrame)
    assert from_records.call_args.kwargs["format"] == "dataframe"
