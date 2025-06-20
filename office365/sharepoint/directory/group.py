from __future__ import annotations

from typing import TYPE_CHECKING

from office365.sharepoint.directory.helper import SPHelper
from office365.sharepoint.directory.members_info import MembersInfo
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection

if TYPE_CHECKING:
    from office365.directory.users.user import User


class Group(Entity):
    """Represents a directory group in SharePoint."""

    def get_members_info(self, row_limit: int) -> MembersInfo:
        """Gets information about the group members.

        Args:
            row_limit: Maximum number of members to return

        Returns:
            MembersInfo object containing member information
        """
        return_type = MembersInfo(self.context)

        def _get_members_info():
            from office365.sharepoint.directory.helper import SPHelper

            SPHelper.get_members_info(
                self.context, self.properties["Id"], row_limit, return_type
            )

        self.ensure_property("Id", _get_members_info)
        return return_type

    def get_members(self):
        """Gets the group's members.

        Returns:
            Collection of User objects representing group members
        """
        from office365.directory.users.user import User

        return_type = EntityCollection(self.context, User)

        def _group_loaded():
            SPHelper.get_members(self.context, self.properties["Id"], return_type)

        self.ensure_property("Id", _group_loaded)
        return return_type

    def get_owners(self) -> EntityCollection[User]:
        """Gets the group's owners.

        Returns:
            Collection of User objects representing group owners
        """
        from office365.directory.users.user import User

        return_type = EntityCollection(self.context, User)

        def _get_owners():
            SPHelper.get_owners(self.context, self.properties["Id"], return_type)

        self.ensure_property("Id", _get_owners)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.Directory.Group"
