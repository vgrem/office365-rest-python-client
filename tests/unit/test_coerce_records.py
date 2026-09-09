"""Offline tests for record-import column handling (dynamic vs typed entities)."""

from __future__ import annotations

import warnings

from office365.directory.users.user import User
from office365.runtime.converters.csv_reader import coerce_records
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.collection import ListItemCollection
from office365.sharepoint.listitems.listitem import ListItem
from tests import test_site_url


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
