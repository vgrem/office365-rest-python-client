from typing import Optional

from office365.runtime.paths.resource_path import ResourcePath
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

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "RoleDefinitionBindings": self.role_definition_bindings,
            }
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)
