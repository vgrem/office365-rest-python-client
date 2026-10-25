from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class StorageEntity(Entity):
    """Storage entities which are available across app catalog scopes."""

    @odata(name="Value")
    @property
    def value(self):
        """The value inside the storage entity."""
        return self.properties.get("Value", None)

    @odata(name="Comment")
    @property
    def comment(self) -> Optional[str]:
        """Gets the Comment property"""
        return self.properties.get("Comment", None)

    @odata(name="Description")
    @property
    def description(self) -> Optional[str]:
        """Gets the Description property"""
        return self.properties.get("Description", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ClientSideComponent.StorageEntity"
