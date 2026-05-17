from typing import Optional

from office365.directory.extensions.extension import Extension
from office365.directory.objects.object import DirectoryObject
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class AdministrativeUnit(DirectoryObject):
    """
    An administrative unit provides a conceptual container for user, group, and device directory objects.
    Using administrative units, a company administrator can now delegate administrative responsibilities to manage
    the users, groups, and devices contained within or scoped to an administrative unit to a regional or
    departmental administrator. This resource is an open type that allows other properties to be passed in.
    """

    def __str__(self):
        return self.display_name or self.entity_type_name

    @property
    def display_name(self) -> Optional[str]:
        """Display name for the administrative unit"""
        return self.properties.get("displayName", None)

    @property
    def visibility(self):
        """
        Controls whether the administrative unit and its members are hidden or public. Can be set to HiddenMembership.
        If not set (value is null), the default behavior is public. When set to HiddenMembership, only members of
        the administrative unit can list other members of the administrative unit.
        """
        return self.properties.get("visibility", None)

    @property
    def members(self):
        """Users and groups that are members of this administrative unit"""
        from office365.directory.objects.collection import DirectoryObjectCollection

        return self.properties.get(
            "members",
            DirectoryObjectCollection(self.context, ResourcePath("members", self.resource_path)),
        )

    @property
    def extensions(self) -> EntityCollection[Extension]:
        """The collection of open extensions defined for this administrative unit."""
        return self.properties.get(
            "extensions",
            EntityCollection(self.context, Extension, ResourcePath("extensions", self.resource_path)),
        )
