from typing import Optional

from office365.directory.objects.object import DirectoryObject
from office365.runtime.types.odata_property import odata


class DirectoryRoleTemplate(DirectoryObject):
    """Represents a directory role template. A directory role template specifies the property values of a directory
    role (directoryRole)."""

    def __repr__(self) -> str:
        return self.display_name or ""

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """The display name to set for the directory role"""
        return self.properties.get("displayName", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """The display name to set for the directory role"""
        return self.properties.get("description", None)
