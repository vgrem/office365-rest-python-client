from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.sharepoint.fields.field import Field


class ViewFieldCollection(Entity):
    """Represents a collection of Field resources."""

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index: int) -> str:
        """Gets view field by index"""
        return self.items[index]

    def __repr__(self):
        return repr(self.items)

    @property
    def schema_xml(self) -> Optional[str]:
        """Gets Schema Xml."""
        return self.properties.get("SchemaXml", None)

    @property
    def items(self) -> Optional[List[str]]:
        """Gets items."""
        return self.properties.get("Items", None)

    def set_property(self, name, value, persist_changes=False):
        if name == "Items":
            value = list(value.values())
        super(ViewFieldCollection, self).set_property(name, value, persist_changes)
        return self

    def add_view_field(self, field: Union[str, Field]) -> Self:
        """
        Adds the field with the specified field internal name or display name to the collection.
        :param str field:
        """
        from office365.sharepoint.fields.field import Field

        def _add_view_field(field_name: str) -> Self:
            """
            Adds the field with the specified field internal name or display name to the collection.
            """
            qry = ServiceOperationQuery(self, "AddViewField", [field_name])
            self.context.add_query(qry)

        if isinstance(field, Field):
            field.ensure_property(
                "InternalName", lambda: _add_view_field(field.internal_name)
            )
        else:
            _add_view_field(field)
        return self

    def move_view_field_to(self, field: Union[str, Field], index: int) -> Self:
        """
        Moves the field with the specified field internal name to the specified position in the collection
        :param str field: Specifies the field internal name.
        :param int index: Specifies the new position for the field (2). The first position is 0.
        """
        from office365.sharepoint.fields.field import Field

        def _move_view_field_to(field_name: str) -> Self:
            params = {"field": field_name, "index": index}
            qry = ServiceOperationQuery(self, "MoveViewFieldTo", None, params)
            self.context.add_query(qry)

        if isinstance(field, Field):
            field.ensure_property(
                "InternalName", lambda: _move_view_field_to(field.internal_name)
            )
        else:
            _move_view_field_to(field)

        return self

    def remove_all_view_fields(self) -> Self:
        """Removes all the fields from the collection."""
        qry = ServiceOperationQuery(self, "RemoveAllViewFields")
        self.context.add_query(qry)
        return self

    def remove_view_field(self, field: Union[str, Field]) -> Self:
        """
        Removes the field with the specified field internal name or display name from the collection.
        :param str field:
        """
        from office365.sharepoint.fields.field import Field

        def _remove_view_field(field_name: str) -> Self:
            qry = ServiceOperationQuery(self, "RemoveViewField", [field_name])
            self.context.add_query(qry)

        if isinstance(field, Field):
            field.ensure_property(
                "InternalName", lambda: _remove_view_field(field.internal_name)
            )
        else:
            _remove_view_field(field)

        return self

    @property
    def entity_type_name(self):
        return "SP.ViewFieldCollection"
