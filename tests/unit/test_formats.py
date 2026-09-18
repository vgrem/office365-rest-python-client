"""Unit tests for the data-pipeline formats and path|IO parity.

Covers tsv/json/ndjson (stdlib), parquet/orc/feather (pyarrow), and SQL/DuckDB
streaming — optional formats are skipped when their dependency is absent.
"""

from __future__ import annotations

import pytest
from office365.directory.users.user import User
from office365.graph_client import GraphClient
from office365.runtime.converters import registry
from office365.runtime.record_collection import RecordCollection

RECORDS = [
    {"userPrincipalName": "a@contoso.com", "displayName": "A", "accountEnabled": True},
    {"userPrincipalName": "b@contoso.com", "displayName": "B", "accountEnabled": False},
]


def _collection(records):
    col = RecordCollection(GraphClient(), User, None)
    for props in records:
        col.add_child(col.create_typed_object(props))
    col.query_options.select = list(records[0].keys())
    return col


def test_writer_accepts_a_path_and_reader_reads_it(tmp_path):
    path = tmp_path / "data.csv"

    registry.writer_for("csv")(_collection(RECORDS), str(path))

    assert path.exists()
    records = registry.reader_for("csv")(str(path))
    assert [r["displayName"] for r in records] == ["A", "B"]


def test_tsv_writer_and_reader(tmp_path):
    path = tmp_path / "data.tsv"

    registry.writer_for("tsv")(_collection(RECORDS), str(path))

    assert "\t" in path.read_text(encoding="utf-8")
    records = registry.reader_for("tsv")(str(path))
    assert [r["displayName"] for r in records] == ["A", "B"]


@pytest.mark.parametrize("fmt", ["parquet", "orc", "feather"])
def test_pyarrow_formats_round_trip(tmp_path, fmt):
    pytest.importorskip("pyarrow")
    path = tmp_path / f"data.{fmt}"

    registry.writer_for(fmt)(_collection(RECORDS), str(path))

    records = registry.reader_for(fmt)(str(path))
    assert [r["displayName"] for r in records] == ["A", "B"]


def test_streaming_csv_writer_appends_pages(tmp_path):
    from office365.runtime.converters.streamers import streamer_for

    path = tmp_path / "out.csv"
    stream = streamer_for("csv")(str(path))
    stream.write([{"a": 1, "b": "x"}])
    stream.write([{"a": 2, "b": "y"}])
    stream.close()

    assert path.read_text(encoding="utf-8").count("a,b") == 1  # header written once
    assert [r["a"] for r in registry.reader_for("csv")(str(path))] == ["1", "2"]


def test_streaming_json_writer_appends_pages(tmp_path):
    import json

    from office365.runtime.converters.streamers import streamer_for

    path = tmp_path / "out.json"
    stream = streamer_for("json")(str(path))
    stream.write([{"a": 1}])
    stream.write([{"a": 2}])
    stream.close()

    assert json.loads(path.read_text(encoding="utf-8")) == [{"a": 1}, {"a": 2}]


def test_records_from_items_projects_selected_fields():
    from office365.runtime.converters.records import records_from_items

    records = records_from_items(list(_collection(RECORDS)), ["displayName"], [])

    assert records == [{"displayName": "A"}, {"displayName": "B"}]


def test_duckdb_streaming_and_write():
    duckdb = pytest.importorskip("duckdb")
    from office365.runtime.converters.sql import duckdb_chunks, write_duckdb

    con = duckdb.connect()
    con.execute("CREATE TABLE src AS SELECT 'A' AS displayName, 1 AS n")

    assert list(duckdb_chunks(con, "SELECT * FROM src", 1)) == [[{"displayName": "A", "n": 1}]]

    write_duckdb(RECORDS, con, table="dst")
    assert con.execute("SELECT count(*) FROM dst").fetchone()[0] == len(RECORDS)  # noqa: PLR2004


def test_sql_streaming_and_write():
    sqlalchemy = pytest.importorskip("sqlalchemy")
    pytest.importorskip("pandas")
    from office365.runtime.converters.sql import sql_chunks, write_sql

    engine = sqlalchemy.create_engine("sqlite://")
    write_sql(RECORDS, engine, table="users", index=False)

    batches = list(sql_chunks(engine, "SELECT * FROM users", 1))
    assert sum(len(batch) for batch in batches) == len(RECORDS)  # noqa: PLR2004
