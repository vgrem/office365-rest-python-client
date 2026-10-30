from office365.entity_collection import EntityCollection
from office365.onedrive.base_item import BaseItem
from office365.onedrive.recyclebin.item import RecycleBinItem
from office365.onedrive.recyclebin.settings import RecycleBinSettings
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class RecycleBin(BaseItem):
    """Represents a container for a collection of recycleBinItem resources in a SharePoint site or a
    SharePoint Embedded fileStorageContainer."""

    @odata(name="items", navigation=True)
    @property
    def items(self) -> EntityCollection[RecycleBinItem]:
        """List of the recycleBinItems deleted by a user."""
        return self.properties.setdefault(
            "items", EntityCollection(self.context, RecycleBinItem, ResourcePath("items", self.resource_path), self)
        )

    @odata(name="settings")
    @property
    def settings(self) -> RecycleBinSettings:
        """Settings for the recycleBin"""
        return self.properties.get("settings", RecycleBinSettings())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RecycleBin"
