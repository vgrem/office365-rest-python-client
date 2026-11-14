"""Both ends of the pipeline: the format table, and the file bridge that feeds it.

A collection leaves as any format the registry knows - synchronously, page by page, or through a
stream that is closed even when the next page fails - and it arrives from a spreadsheet that lives
in SharePoint. The optional dependencies are skipped, not faked: a format that is not installed is
a format nobody can be wrong about.
"""

from __future__ import annotations

import json
from unittest import mock

import pytest
from office365.directory.users.user import User
from office365.migration.offline import offline_sharepoint_context
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
