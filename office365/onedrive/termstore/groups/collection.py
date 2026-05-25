from typing import cast

from office365.directory.permissions.require_permission import require_permission
from office365.entity_collection import EntityCollection
from office365.onedrive.termstore.groups.group import Group


class GroupCollection(EntityCollection[Group]):
    def __init__(self, context, resource_path=None):
        super().__init__(context, Group, resource_path)

    @require_permission(
        delegated=["TermStore.ReadWrite.All"],
        application=["TermStore.ReadWrite.All"],
        notes="Create a new term store group",
    )
    def add(self, display_name: str) -> Group:
        """
        Create a new group object in a term store.
        :param str display_name: Name of the group to be created.
        """
        props = {"displayName": display_name}
        return super().add(**props)

    @require_permission(
        delegated=["TermStore.Read.All", "TermStore.ReadWrite.All"],
        application=["TermStore.Read.All", "TermStore.ReadWrite.All"],
        notes="Get a term store group by name",
    )
    def get_by_name(self, name: str) -> Group:
        """Returns the group with the specified name."""
        return cast(Group, self.single(f"displayName eq '{name}'"))
