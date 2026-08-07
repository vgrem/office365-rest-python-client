from typing import Optional

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions.roles.definitions.collection import (
    RoleDefinitionCollection,
)
from office365.sharepoint.principal.principal import Principal


class RoleAssignment(Entity):
    """An association between a principal or a site group and a role definition."""

    @property
    def principal_id(self) -> Optional[int]:
        """Specifies the identifier of the user or group corresponding to the role assignment."""
        return self.properties.get("PrincipalId", None)

    @property
    def member(self) -> Principal:
        """Specifies the user or group corresponding to the role assignment."""
        return self.properties.get(
            "Member",
            Principal(self.context, ResourcePath("Member", self.resource_path)),
        )

    @odata(name="RoleDefinitionBindings")
    @property
    def role_definition_bindings(self) -> RoleDefinitionCollection:
        """Specifies a collection of role definitions for this role assignment."""
        return self.properties.get(
            "RoleDefinitionBindings",
            RoleDefinitionCollection(self.context, ResourcePath("RoleDefinitionBindings", self.resource_path)),
        )

    @property
    def property_ref_name(self) -> str:
        return "PrincipalId"
