"""Offline tests for the pandas bridge — skipped without the optional 'pandas' extra."""

# ruff: noqa: E402  (imports must follow the importorskip guard)

from __future__ import annotations

from typing import cast

import pytest

pd = pytest.importorskip("pandas")

from office365.directory.users.user import User
from office365.graph_client import GraphClient
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.converters.dataframe import (
    DataFrameResult,
    read_dataframe,
    records_from_dataframe,
    series_kind,
    write_dataframe,
)
from office365.sharepoint.fields.type import FieldType
from office365.sharepoint.lists.list import _field_kind, _sanitize_field_name


def _collection(properties: list[dict], context=None) -> ClientObjectCollection:
    col = ClientObjectCollection(context or cast(ClientRuntimeContext, None), User, None)
    for props in properties:
        col.add_child(col.create_typed_object(props))
    return col


def test_write_dataframe():
    col = _collection(
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
    col = _collection(
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
    col = _collection([{"displayName": "John Doe"}], context=client)
    result = col.to_dataframe()
    assert isinstance(result, DataFrameResult)
    # the after_execute callback materializes .value on the loaded collection
    write_dataframe(col, result)
    assert list(result.value.columns) == ["displayName"]


def test_records_from_dataframe_drops_nan_cells():
    df = pd.DataFrame({"a": [1.0, float("nan")], "b": ["x", "y"]})
    assert records_from_dataframe(df) == [{"a": 1.0, "b": "x"}, {"b": "y"}]


def test_records_from_dataframe_renames_keys():
    df = pd.DataFrame({"Median Income": [8.3]})
    assert records_from_dataframe(df, key_fn=_sanitize_field_name) == [{"Median_Income": 8.3}]


def test_sanitize_field_name():
    assert _sanitize_field_name("Median Income") == "Median_Income"
    assert _sanitize_field_name("a/b?c") == "a_b_c"


def test_field_kind_mapping():
    assert _field_kind(pd, pd.Series([True])) is FieldType.Boolean
    assert _field_kind(pd, pd.Series(pd.to_datetime(["2025-01-01"]))) is FieldType.DateTime
    assert _field_kind(pd, pd.Series([1.5])) is FieldType.Number
    assert _field_kind(pd, pd.Series(["text"])) is FieldType.Text


def test_series_kind():
    assert series_kind(pd, pd.Series([True])) == "boolean"
    assert series_kind(pd, pd.Series(pd.to_datetime(["2025-01-01"]))) == "datetime"
    assert series_kind(pd, pd.Series([1.5])) == "number"
    assert series_kind(pd, pd.Series(["text"])) == "text"
