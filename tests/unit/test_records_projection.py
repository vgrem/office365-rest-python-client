"""The record projection asks the type, not the page it happens to have read.

A record is a row of the model, so its columns have to be the ones the serializer,
``$select`` and the migration imports already agree on. Reading the response instead
answered a different question -- the keys one page happened to carry, sorted -- so an
item with an extra field reordered every header, and a declared column the service
left out of a page vanished rather than arriving empty.
"""

from __future__ import annotations

from typing import Any, List

import pytest
from office365.directory.users.user import User
from office365.outlook.mail.messages.message import Message
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.converters.records import declared_columns, iter_records
from office365.runtime.schema import TypeSchema


class _Client:
    """A client that addresses one version, as ``GraphClient`` does."""

    version = "v1.0"


def _collection(properties: List[dict], item_type: type = User, context: Any = None) -> ClientObjectCollection:
    col = ClientObjectCollection(context, item_type, None)
    for props in properties:
        col.add_child(col.create_typed_object(props))
    return col


def test_headers_are_the_declared_columns_even_when_the_page_omits_them() -> None:
    columns = TypeSchema.of(User).columns
    record = iter_records(_collection([{columns[0]: "a value"}]))[0]

    assert list(record) == list(columns), "declaration order, and every column present"
    assert record[columns[0]] == "a value"
    assert record[columns[1]] is None, "a column the page omitted is empty, not missing"


def test_a_name_the_metadata_does_not_describe_still_follows() -> None:
    """A list item's site columns exist on the wire and not in the CSDL."""
    columns = TypeSchema.of(User).columns
    record = iter_records(_collection([{columns[0]: "a value", "siteColumn": "kept"}]))[0]

    assert list(record) == [*columns, "siteColumn"]


def test_an_extra_field_appends_without_reordering_the_declared_ones() -> None:
    """The whole defect: one page's extra column used to move every header."""
    columns = TypeSchema.of(User).columns
    page = _collection([{columns[0]: "a"}, {columns[0]: "b", "extra": 1}])
    records = iter_records(page)

    for record in records:
        assert list(record)[: len(columns)] == list(columns)
    assert list(records[0]) == [*columns, "extra"]


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


def test_the_columns_are_the_ones_the_projection_reports() -> None:
    page = _collection([{"id": "1"}], Message, _Client())

    assert declared_columns(list(page)) == list(iter_records(page)[0])


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
