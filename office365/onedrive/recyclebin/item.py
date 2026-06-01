from datetime import datetime
from typing import Optional

from office365.onedrive.base_item import BaseItem
from office365.runtime.types.odata_property import odata


class RecycleBinItem(BaseItem):
    """Represents information about a deleted item in a recycleBin of a SharePoint site or a SharePoint
    Embedded fileStorageContainer."""

    @odata(name="deletedDateTime")
    @property
    def deleted_datetime(self) -> Optional[datetime]:
        """Date and time when the item was deleted. The timestamp type represents date and time information using
        ISO 8601 format and is always in UTC."""
        return self.properties.get("deletedDateTime", datetime.min)

    @property
    def deleted_from_location(self) -> Optional[str]:
        """Relative URL of the list or folder that originally contained the item."""
        return self.properties.get("deletedFromLocation", None)

    @property
    def size(self) -> Optional[int]:
        """Size of the item in bytes."""
        return self.properties.get("size", None)

    @property
    def deleted_date_time(self) -> datetime:
        """Gets the deletedDateTime property"""
        return self.properties.get("deletedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RecycleBinItem"
