from datetime import datetime
from typing import Optional

from office365.onedrive.base_item import BaseItem


class RecycleBinItem(BaseItem):
    """Represents information about a deleted item in a recycleBin of a SharePoint site or a SharePoint
    Embedded fileStorageContainer.
    """

    @property
    def deleted_datetime(self):
        # type: () -> Optional[datetime]
        """Date and time when the item was deleted. The timestamp type represents date and time information using
        ISO 8601 format and is always in UTC.
        """
        return self.properties.get("deletedDateTime", datetime.min)

    @property
    def deleted_from_location(self):
        # type: () -> Optional[str]
        """Relative URL of the list or folder that originally contained the item."""
        return self.properties.get("deletedFromLocation", None)

    @property
    def size(self):
        # type: () -> Optional[int]
        """Size of the item in bytes."""
        return self.properties.get("size", None)

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "deletedDateTime": self.deleted_datetime,
            }
            default_value = property_mapping.get(name, None)
        return super(BaseItem, self).get_property(name, default_value)
