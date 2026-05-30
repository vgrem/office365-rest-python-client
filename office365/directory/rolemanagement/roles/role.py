from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.directory.objects.object import DirectoryObject
from office365.directory.permissions.scoped_role_membership import ScopedRoleMembership
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath

if TYPE_CHECKING:
    from office365.directory.objects.collection import DirectoryObjectCollection


class DirectoryRole(DirectoryObject):
    """Represents an Azure AD directory role. Azure AD directory roles are also known as administrator roles"""

    def __repr__(self):
        return self.id or self.entity_type_name

    def __str__(self):
        return f"Name: {self.display_name}"

    def add_member(self, user_principal_name: str) -> Self:
        """Add a user to this directory role by their user principal name.

        :param str user_principal_name: The UPN (e.g. 'user@contoso.com')
        """

        def _add(user: DirectoryObject) -> None:
            self.members.add(user)

        self.context.users.get_by_principal_name(user_principal_name).get().after_execute(_add)
        return self

    def remove_member(self, user_principal_name: str) -> Self:
        """Remove a user from this directory role by their user principal name.

        :param str user_principal_name: The UPN (e.g. 'user@contoso.com')
        """

        def _remove(user: DirectoryObject) -> None:
            self.members.remove(user)

        self.context.users.get_by_principal_name(user_principal_name).get().after_execute(_remove)
        return self

    @property
    def description(self) -> Optional[str]:
        """The description for the directory role."""
        return self.properties.get("Description", None)

    @property
    def display_name(self) -> Optional[str]:
        """The display name for the directory role."""
        return self.properties.get("displayName", None)

    @property
    def members(self) -> DirectoryObjectCollection:
        """Users that are members of this directory role."""
        from office365.directory.objects.collection import DirectoryObjectCollection

        return self.properties.get(
            "members",
            DirectoryObjectCollection(self.context, ResourcePath("members", self.resource_path)),
        )

    @property
    def role_template_id(self) -> Optional[str]:
        return self.properties.get("roleTemplateId", None)

    @property
    def scoped_members(self) -> EntityCollection[ScopedRoleMembership]:
        """Members of this directory role that are scoped to administrative units."""

        return self.properties.get(
            "scopedMembers",
            EntityCollection(
                self.context,
                ScopedRoleMembership,
                ResourcePath("scopedMembers", self.resource_path),
            ),
        )
