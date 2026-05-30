from typing_extensions import Self

from office365.delta_collection import DeltaCollection
from office365.directory.rolemanagement.roles.role import DirectoryRole
from office365.directory.rolemanagement.templates.collection import DirectoryRoleTemplateCollection
from office365.directory.rolemanagement.templates.template import DirectoryRoleTemplate


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

    def assign(self, role_name: str) -> Self:
        """Activate a directory role by display name.

        Idempotent — if already activated, the server returns 409 Conflict.
        The caller can catch and ignore it.

        :param str role_name: The display name (e.g. 'Security Administrator')
        """

        def _assign(templates: DirectoryRoleTemplateCollection) -> None:
            template: DirectoryRoleTemplate | None = next(
                (t for t in templates if t.display_name == role_name), None
            )
            assert template is not None and template.id is not None
            self.add(roleTemplateId=template.id)

        self.context.directory_role_templates.get().after_execute(_assign)
        return self
