from datetime import datetime
from typing import Optional

from office365.sharepoint.changes.token import ChangeToken
from office365.sharepoint.changes.type import ChangeType
from office365.sharepoint.entity import Entity


class Change(Entity):
    """Base class for a change. installation."""

    @property
    def change_type_name(self) -> str:
        return self.change_type.name

    @property
    def change_token(self) -> ChangeToken:
        """Returns an ChangeToken that represents the change."""
        return self.properties.get("ChangeToken", ChangeToken())

    @property
    def change_type(self) -> ChangeType:
        """
        Returns an SPChangeType that indicates the type of change, including adding, updating, deleting, or renaming
        changes, but also moving items away from or into lists and folders.
        """
        return self.properties.get("ChangeType", ChangeType.None_)

    @property
    def site_id(self) -> Optional[str]:
        """
        Returns the Id of the site of the changed item
        """
        return self.properties.get("SiteId", None)

    @property
    def time(self) -> datetime:
        """
        Gets a value that specifies the time that the object was modified.
        """
        return self.properties.get("Time", datetime.min)

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "ChangeType": self.change_type,
                "ChangeToken": self.change_token,
            }
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)
