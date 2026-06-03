from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.resource_environment import (
    AccessPackageResourceEnvironment,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.resource_role import (
    AccessPackageResourceRole,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.resource_scope import (
    AccessPackageResourceScope,
)
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class AccessPackageResource(Entity):
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def modified_date_time(self) -> datetime:
        """Gets the modifiedDateTime property"""
        return self.properties.get("modifiedDateTime", datetime.min)

    @property
    def origin_id(self) -> Optional[str]:
        """Gets the originId property"""
        return self.properties.get("originId", None)

    @property
    def origin_system(self) -> Optional[str]:
        """Gets the originSystem property"""
        return self.properties.get("originSystem", None)

    @property
    def environment(self) -> AccessPackageResourceEnvironment:
        """Gets the environment property"""
        return self.properties.get(
            "environment",
            AccessPackageResourceEnvironment(self.context, ResourcePath("environment", self.resource_path)),
        )

    @property
    def roles(self) -> EntityCollection[AccessPackageResourceRole]:
        """Gets the roles property"""
        return self.properties.get(
            "roles",
            EntityCollection[AccessPackageResourceRole](
                self.context, AccessPackageResourceRole, ResourcePath("roles", self.resource_path)
            ),
        )

    @property
    def scopes(self) -> EntityCollection[AccessPackageResourceScope]:
        """Gets the scopes property"""
        return self.properties.get(
            "scopes",
            EntityCollection[AccessPackageResourceScope](
                self.context, AccessPackageResourceScope, ResourcePath("scopes", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageResource"
