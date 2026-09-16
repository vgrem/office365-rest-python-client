"""SharePoint list-item :class:`UpsertTarget` — the destination side of keyed imports.

Keeps the SharePoint-specific pieces (ensure the key column, load existing keys,
create/update items) out of the runtime upsert core, so the same
:func:`~office365.runtime.converters.upsert.keyed_queue` drives list imports and
the migration toolkit.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, cast

from office365.runtime.paths.v3.entity import EntityPath
from office365.sharepoint.fields.type import FieldType
from office365.sharepoint.listitems.listitem import ListItem

if TYPE_CHECKING:
    from office365.sharepoint.listitems.collection import ListItemCollection
    from office365.sharepoint.lists.list import List


class ListItemUpsertTarget:
    """Keyed skip/upsert target backed by a :class:`ListItemCollection`."""

    def __init__(
        self,
        collection: "ListItemCollection",
        *,
        key_field: str = "MigrationKey",
        enforce_unique: bool = False,
    ) -> None:
        self._collection = collection
        self._key_field = key_field
        self._enforce_unique = enforce_unique

    @property
    def key_field(self) -> str:
        return self._key_field

    def ensure_key_field(self) -> None:
        """Queue the key column (Text, optionally unique+indexed) if missing."""
        from office365.sharepoint.fields.creation_information import FieldCreationInformation

        parent = cast("List", self._collection.parent)
        if parent is None:
            return
        field = parent.fields.ensure(FieldCreationInformation(Title=self._key_field, FieldTypeKind=FieldType.Text))
        if self._enforce_unique:
            field.set_property("EnforceUniqueValues", True)
            field.set_property("Indexed", True)
            field.update()

    def load_keys(self) -> Mapping[str, Any]:
        """Return the existing ``{key: item_id}`` map (paged; key + ``Id`` only)."""
        loaded = self._collection.select([self._key_field, "Id"]).get_all().execute_query()
        keys: dict[str, Any] = {}
        for item in loaded:
            value = item.properties.get(self._key_field)
            item_id = item.id
            if value is not None and item_id is not None:
                keys[str(value)] = item_id
        return keys

    def create_records(self, records: list[dict]) -> None:
        self._collection.from_records(records)

    def update_record(self, item_id: Any, record: dict) -> None:
        item = ListItem(
            self._collection.context,
            EntityPath(item_id, self._collection.resource_path),
            parent_list=self._collection.parent,
        )
        for name, value in record.items():
            item.set_property(name, value, persist_changes=True)
        item.update()
