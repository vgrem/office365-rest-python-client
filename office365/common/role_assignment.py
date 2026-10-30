from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.common.role_definition import RoleDefinition


class RoleAssignment(Entity):
    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="resourceScopes")
    @property
    def resource_scopes(self) -> StringCollection:
        """Gets the resourceScopes property"""
        return self.properties.get("resourceScopes", StringCollection())

    @odata(name="roleDefinition", navigation=True)
    @property
    def role_definition(self) -> RoleDefinition:
        """Gets the roleDefinition property"""
        from office365.common.role_definition import RoleDefinition

        return self.properties.get(
            "roleDefinition", RoleDefinition(self.context, ResourcePath("roleDefinition", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RoleAssignment"
