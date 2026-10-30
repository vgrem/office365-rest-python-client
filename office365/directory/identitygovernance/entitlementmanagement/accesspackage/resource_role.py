from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.directory.role_type import RoleType
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.entitlementmanagement.accesspackage.resource import (
        AccessPackageResource,
    )


class AccessPackageResourceRole(Entity):
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

    @odata(name="originId")
    @property
    def origin_id(self) -> Optional[str]:
        """Gets the originId property"""
        return self.properties.get("originId", None)

    @odata(name="originSystem")
    @property
    def origin_system(self) -> Optional[str]:
        """Gets the originSystem property"""
        return self.properties.get("originSystem", None)

    @odata(name="resource", navigation=True)
    @property
    def resource(self) -> AccessPackageResource:
        """Gets the resource property"""
        return self.properties.get(
            "resource", AccessPackageResource(self.context, ResourcePath("resource", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageResourceRole"

    @odata(name="type")
    @property
    def type(self) -> RoleType:
        """Gets the type property"""
        return self.properties.get("type", RoleType.active)
