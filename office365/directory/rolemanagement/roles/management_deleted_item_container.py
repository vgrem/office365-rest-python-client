from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.rolemanagement.unifiedrole.definition import UnifiedRoleDefinition


class DirectoryRoleManagementDeletedItemContainer(Entity):
    @odata(name="roleDefinitions", navigation=True)
    @property
    def role_definitions(self) -> EntityCollection[UnifiedRoleDefinition]:
        """Gets the roleDefinitions property"""
        from office365.directory.rolemanagement.unifiedrole.definition import UnifiedRoleDefinition

        return self.properties.get(
            "roleDefinitions",
            EntityCollection[UnifiedRoleDefinition](
                self.context, UnifiedRoleDefinition, ResourcePath("roleDefinitions", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DirectoryRoleManagementDeletedItemContainer"
