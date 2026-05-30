from office365.delta_collection import DeltaCollection
from office365.directory.rolemanagement.role import DirectoryRole


class DirectoryRoleCollection(DeltaCollection[DirectoryRole]):
    """User's collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, DirectoryRole, resource_path)

    def get_by_name(self, name: str) -> DirectoryRole:
        """Retrieve a directory role by its display name.

        :param str name: The display name (e.g. 'Security Administrator')
        :return: The matching DirectoryRole
        :raises NotFoundException: If no role matches
        :raises ValueError: If multiple roles match
        """
        return self.single(f"displayName eq '{name}'")
