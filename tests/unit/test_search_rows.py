"""Offline tests for the SharePoint search row accessors.

``SearchResult.rows`` / ``RelevantResults.rows`` reach the primary result table,
and ``SimpleDataRow.get`` / ``as_dict`` expose a row's cells without the raw
nested ``Table.Rows[..].Cells`` walk.
"""

from __future__ import annotations

from office365.sharepoint.search.relevant_results import RelevantResults
from office365.sharepoint.search.result import SearchResult
from office365.sharepoint.search.simple_data_row import SimpleDataRow
from office365.sharepoint.search.simple_data_table import SimpleDataTable


def test_simple_data_row_get_and_as_dict():
    row = SimpleDataRow(Cells={"Title": "Hello", "Path": "/x"})

    assert row.get("Title") == "Hello"
    assert row.get("Missing") is None
    assert row.get("Missing", "fallback") == "fallback"
    assert row.as_dict() == {"Title": "Hello", "Path": "/x"}


def test_simple_data_row_as_dict_is_a_copy():
    row = SimpleDataRow(Cells={"Title": "Hello"})

    row.as_dict()["Title"] = "Changed"

    assert row.get("Title") == "Hello"


def test_relevant_results_rows_returns_table_rows():
    table = SimpleDataTable()
    table.Rows.add(SimpleDataRow(Cells={"Title": "A"}))
    results = RelevantResults(Table=table)

    assert len(results.rows) == 1
    assert results.rows[0].get("Title") == "A"


def test_search_result_rows_reaches_primary_result_table():
    search_result = SearchResult()
    search_result.PrimaryQueryResult.RelevantResults.Table.Rows.add(SimpleDataRow(Cells={"Title": "B"}))

    assert len(search_result.rows) == 1
    assert search_result.rows[0].get("Title") == "B"
