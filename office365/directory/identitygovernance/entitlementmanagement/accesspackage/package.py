from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.groups.group import Group
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.entitlementmanagement.accesspackage.assignment_policy import (
        AccessPackageAssignmentPolicy,
    )
    from office365.directory.identitygovernance.entitlementmanagement.accesspackage.catalog import (
        AccessPackageCatalog,
    )
    from office365.directory.identitygovernance.entitlementmanagement.accesspackage.resource_role_scope import (
        AccessPackageResourceRoleScope,
    )


class AccessPackage(Entity):
    @odata(name="catalogId", beta=True)
    @property
    def catalog_id(self) -> Optional[str]:
        """Gets the catalogId property"""
        return self.properties.get("catalogId", None)

    @odata(name="createdBy", beta=True)
    @property
    def created_by(self) -> Optional[str]:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", None)

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
    def is_hidden(self) -> Optional[bool]:
        """Gets the isHidden property"""
        return self.properties.get("isHidden", None)

    @odata(name="isRoleScopesVisible", beta=True)
    @property
    def is_role_scopes_visible(self) -> Optional[bool]:
        """Gets the isRoleScopesVisible property"""
        return self.properties.get("isRoleScopesVisible", None)

    @odata(name="modifiedBy", beta=True)
    @property
    def modified_by(self) -> Optional[str]:
        """Gets the modifiedBy property"""
        return self.properties.get("modifiedBy", None)

    @property
    def modified_date_time(self) -> datetime:
        """Gets the modifiedDateTime property"""
        return self.properties.get("modifiedDateTime", datetime.min)

    @odata(name="uniqueName", beta=True)
    @property
    def unique_name(self) -> Optional[str]:
        """Gets the uniqueName property"""
        return self.properties.get("uniqueName", None)

    @property
    def access_packages_incompatible_with(self) -> EntityCollection[AccessPackage]:
        """Gets the accessPackagesIncompatibleWith property"""
        return self.properties.get(
            "accessPackagesIncompatibleWith",
            EntityCollection[AccessPackage](
                self.context, AccessPackage, ResourcePath("accessPackagesIncompatibleWith", self.resource_path)
            ),
        )

    @property
    def incompatible_access_packages(self) -> EntityCollection[AccessPackage]:
        """Gets the incompatibleAccessPackages property"""
        return self.properties.get(
            "incompatibleAccessPackages",
            EntityCollection[AccessPackage](
                self.context, AccessPackage, ResourcePath("incompatibleAccessPackages", self.resource_path)
            ),
        )

    @property
    def incompatible_groups(self) -> EntityCollection[Group]:
        """Gets the incompatibleGroups property"""
        return self.properties.get(
            "incompatibleGroups",
            EntityCollection[Group](self.context, Group, ResourcePath("incompatibleGroups", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackage"

    @odata(name="assignmentPolicies", beta="accessPackageAssignmentPolicies", navigation=True)
    @property
    def assignment_policies(self) -> EntityCollection[AccessPackageAssignmentPolicy]:
        """Gets the assignmentPolicies property"""
        from office365.directory.identitygovernance.entitlementmanagement.accesspackage.assignment_policy import (
            AccessPackageAssignmentPolicy,
        )

        return self.properties.get(
            "assignmentPolicies",
            EntityCollection[AccessPackageAssignmentPolicy](
                self.context,
                AccessPackageAssignmentPolicy,
                ResourcePath(self.wire_name("assignmentPolicies"), self.resource_path),
            ),
        )

    @odata(name="catalog", beta="accessPackageCatalog", navigation=True)
    @property
    def catalog(self) -> AccessPackageCatalog:
        """Gets the catalog property"""
        from office365.directory.identitygovernance.entitlementmanagement.accesspackage.catalog import (
            AccessPackageCatalog,
        )

        return self.properties.get(
            "catalog",
            AccessPackageCatalog(self.context, ResourcePath(self.wire_name("catalog"), self.resource_path)),
        )

    @odata(name="resourceRoleScopes", beta="accessPackageResourceRoleScopes", navigation=True)
    @property
    def resource_role_scopes(self) -> EntityCollection[AccessPackageResourceRoleScope]:
        """Gets the resourceRoleScopes property"""
        from office365.directory.identitygovernance.entitlementmanagement.accesspackage.resource_role_scope import (
            AccessPackageResourceRoleScope,
        )

        return self.properties.get(
            "resourceRoleScopes",
            EntityCollection[AccessPackageResourceRoleScope](
                self.context,
                AccessPackageResourceRoleScope,
                ResourcePath(self.wire_name("resourceRoleScopes"), self.resource_path),
            ),
        )
