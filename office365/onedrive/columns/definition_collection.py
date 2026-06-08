from __future__ import annotations

from typing import Optional, Union

from typing_extensions import TYPE_CHECKING

from office365.directory.permissions.require_permission import require_permission
from office365.entity_collection import EntityCollection
from office365.onedrive.columns.definition import ColumnDefinition
from office365.runtime.queries.create_entity import CreateEntityQuery

if TYPE_CHECKING:
    from office365.onedrive.lists.list import List


class ColumnDefinitionCollection(EntityCollection[ColumnDefinition]):
    def __init__(self, context, resource_path, parent):
        super().__init__(context, ColumnDefinition, resource_path, parent)

    @require_permission(
        delegated=["Files.ReadWrite.All", "Sites.ReadWrite.All"],
        application=["Files.ReadWrite.All", "Sites.ReadWrite.All"],
        notes="Create a number column",
    )
    def add_number(self, name: str, minimum: float | None = None, maximum: float | None = None):
        """Creates a number column

        Args:
            name (str): The API-facing name of the column as it appears in the fields on a listItem
            minimum (float): The minimum permitted value.
            maximum (float): The maximum permitted value.
        """
        from office365.onedrive.columns.number import NumberColumn

        return self.add(name=name, number=NumberColumn(minimum, maximum))

    @require_permission(
        delegated=["Files.ReadWrite.All", "Sites.ReadWrite.All"],
        application=["Files.ReadWrite.All", "Sites.ReadWrite.All"],
        notes="Create a text column",
    )
    def add_text(self, name: str, max_length: int | None = None, text_type: str | None = None):
        """Creates a text column

        Args:
            name (str): The API-facing name of the column as it appears in the fields on a listItem
            max_length (int or None): The maximum number of characters for the value.
            text_type (str or None): The type of text being stored
        """
        from office365.onedrive.columns.text import TextColumn

        return self.add(name=name, text=TextColumn(maxLength=max_length, textType=text_type))

    @require_permission(
        delegated=["Files.ReadWrite.All", "Sites.ReadWrite.All"],
        application=["Files.ReadWrite.All", "Sites.ReadWrite.All"],
        notes="Create a hyperlink or picture column",
    )
    def add_hyperlink_or_picture(self, name: str, is_picture: bool | None = None):
        """Creates a hyperlink or picture column

        Args:
            name (str): The API-facing name of the column as it appears in the fields on a listItem
            is_picture (bool): Specifies whether the display format used for URL columns is an image or a hyperlink.
        """
        from office365.onedrive.columns.hyperlink_or_picture import (
            HyperlinkOrPictureColumn,
        )

        return self.add(
            name=name,
            hyperlinkOrPicture=HyperlinkOrPictureColumn(isPicture=is_picture),
        )

    @require_permission(
        delegated=["Files.ReadWrite.All", "Sites.ReadWrite.All"],
        application=["Files.ReadWrite.All", "Sites.ReadWrite.All"],
        notes="Create a lookup column referencing another list",
    )
    def add_lookup(
        self,
        name: str,
        lookup_list: Union[List, str],
        column_name: Optional[str] = None,
    ) -> ColumnDefinition:
        """Creates a lookup column

        Args:
            name (str): The API-facing name of the column as it appears in the fields on a listItem
            lookup_list (office365.onedrive.lists.list.List or str): Lookup source list or identifier
            column_name (str): The name of the lookup source column.
        """
        from office365.onedrive.columns.lookup import LookupColumn
        from office365.onedrive.lists.list import List

        if isinstance(lookup_list, List):
            return_type = ColumnDefinition(self.context)
            self.add_child(return_type)

            def _add_lookup():
                params = {
                    "name": name,
                    "lookup": LookupColumn(lookup_list.id, column_name),
                }
                qry = CreateEntityQuery(self, params, return_type)
                self.context.add_query(qry)

            lookup_list.ensure_property("id").after_execute(lambda _: _add_lookup())
            return return_type
        else:
            return self.add(name=name, lookup=LookupColumn(lookup_list, column_name))
