from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class FileStatus(Entity):
    """"""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.FilePublish.Model.FileStatus"

    @odata(name="ErrorCode")
    @property
    def error_code(self) -> Optional[int]:
        """Gets the ErrorCode property"""
        return self.properties.get("ErrorCode", None)

    @odata(name="InitialCreation")
    @property
    def initial_creation(self) -> Optional[bool]:
        """Gets the InitialCreation property"""
        return self.properties.get("InitialCreation", None)

    @odata(name="ListItemId")
    @property
    def list_item_id(self) -> Optional[int]:
        """Gets the ListItemId property"""
        return self.properties.get("ListItemId", None)

    @odata(name="ParentListId")
    @property
    def parent_list_id(self) -> Optional[UUID]:
        """Gets the ParentListId property"""
        return self.properties.get("ParentListId", None)

    @odata(name="Path")
    @property
    def path(self) -> ResourcePath:
        """Gets the Path property"""
        from office365.sharepoint.types.resource_path import ResourcePath

        return self.properties.get("Path", ResourcePath())

    @odata(name="Succeeded")
    @property
    def succeeded(self) -> Optional[bool]:
        """Gets the Succeeded property"""
        return self.properties.get("Succeeded", None)

    @odata(name="UniqueId")
    @property
    def unique_id(self) -> Optional[UUID]:
        """Gets the UniqueId property"""
        return self.properties.get("UniqueId", None)
