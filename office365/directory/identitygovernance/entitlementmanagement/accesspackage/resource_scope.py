from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath

if TYPE_CHECKING:
    from office365.directory.identitygovernance.entitlementmanagement.accesspackage.resource import AccessPackageResource


class AccessPackageResourceScope(Entity):
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def is_root_scope(self) -> Optional[bool]:
        """Gets the isRootScope property"""
        return self.properties.get("isRootScope", None)

    @property
    def origin_id(self) -> Optional[str]:
        """Gets the originId property"""
        return self.properties.get("originId", None)

    @property
    def origin_system(self) -> Optional[str]:
        """Gets the originSystem property"""
        return self.properties.get("originSystem", None)

    @property
    def resource(self) -> AccessPackageResource:
        """Gets the resource property"""
        return self.properties.get(
            "resource", AccessPackageResource(self.context, ResourcePath("resource", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageResourceScope"
