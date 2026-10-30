from typing import Optional

from office365.directory.objects.object import DirectoryObject
from office365.runtime.types.odata_property import odata


class PolicyBase(DirectoryObject):
    """Represents an abstract base type for policy types to inherit from"""

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Display name for this policy"""
        return self.properties.get("displayName", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PolicyBase"
