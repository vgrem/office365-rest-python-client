"""A read of a column is not a write to the record.

The record — ``properties`` — is what ``to_json`` and the export pipeline serialize, so
reading one column may not grow it. ``ListItem.get_property`` used to resolve a handful of
names through a table it built on every call, which evaluated every navigation on every
read; ``parent_list`` caches itself in ``properties`` as soon as it is touched, so reading
``FileRef`` added a ``ParentList`` stub to the record and to the payload.

Every name the table special-cased is declared with ``@odata(name=...)`` on its getter, so
the declaration is all ``get_property`` needs: the base class resolves the wire name to the
attribute and calls it.
"""

from __future__ import annotations

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.list import List


def _item(**properties: object) -> ListItem:
    item = ListItem(ClientContext("https://contoso.sharepoint.com/sites/x"))
    item.properties.update(properties)
    return item


def test_reading_a_declared_column_leaves_the_record_alone() -> None:
    item = _item(FileRef="/sites/x/Shared Documents/a.txt", Title="A")

    assert item.get_property("FileRef") == "/sites/x/Shared Documents/a.txt"
    assert sorted(item.properties) == ["FileRef", "Title"], "a read added a member to the record"
    assert item.to_json() == {"FileRef": "/sites/x/Shared Documents/a.txt", "Title": "A"}


def test_reading_every_selectable_column_leaves_the_record_alone() -> None:
    row = {"UniqueId": "8f2b1c9d-0000-0000-0000-000000000000", "File_x0020_Type": "txt", "ID": 7}
    item = _item(**row)

    for name in ListItem.select_all():
        item.get_property(name)

    assert sorted(item.properties) == sorted(row), "a column getter memoized into the record"


def test_reading_the_navigation_materializes_it() -> None:
    """The laziness is about which name is resolved, not about dropping the default."""
    item = _item()

    assert isinstance(item.get_property("ParentList"), List)
    assert "ParentList" in item.properties, "asking for the navigation is what fills it in"
    assert item.get_property("ParentList") is item.properties["ParentList"], "one stub per item"


def test_a_column_the_metadata_does_not_declare_reads_as_none() -> None:
    """``OData__dlc_DocIdUrl`` is a document-library column, not an item-row one."""
    item = _item()

    assert item.doc_id_url is None
    assert item.get_property("OData__dlc_DocIdUrl") is None
