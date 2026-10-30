from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.permissions.identity import Identity
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.unified_role_management_policy_rule import (
        UnifiedRoleManagementPolicyRule,
    )


class UnifiedRoleManagementPolicy(Entity):
    """Specifies the various policies associated with scopes and roles.
    For policies that apply to Azure RBAC, use the Azure REST PIM API for role management policies.
    """

    def __str__(self):
        return self.display_name or self.entity_type_name

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """
        Display name for the policy.
        """
        return self.properties.get("displayName", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="isOrganizationDefault")
    @property
    def is_organization_default(self) -> Optional[bool]:
        """Gets the isOrganizationDefault property"""
        return self.properties.get("isOrganizationDefault", None)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> Identity:
        """Gets the lastModifiedBy property"""
        return self.properties.get("lastModifiedBy", Identity())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="scopeId")
    @property
    def scope_id(self) -> Optional[str]:
        """Gets the scopeId property"""
        return self.properties.get("scopeId", None)

    @odata(name="scopeType")
    @property
    def scope_type(self) -> Optional[str]:
        """Gets the scopeType property"""
        return self.properties.get("scopeType", None)

    @odata(name="effectiveRules", navigation=True)
    @property
    def effective_rules(self) -> EntityCollection[UnifiedRoleManagementPolicyRule]:
        """Gets the effectiveRules property"""
        from office365.directory.unified_role_management_policy_rule import (
            UnifiedRoleManagementPolicyRule,
        )

        return self.properties.get(
            "effectiveRules",
            EntityCollection[UnifiedRoleManagementPolicyRule](
                self.context, UnifiedRoleManagementPolicyRule, ResourcePath("effectiveRules", self.resource_path)
            ),
        )

    @odata(name="rules", navigation=True)
    @property
    def rules(self) -> EntityCollection[UnifiedRoleManagementPolicyRule]:
        """Gets the rules property"""
        from office365.directory.unified_role_management_policy_rule import (
            UnifiedRoleManagementPolicyRule,
        )

        return self.properties.get(
            "rules",
            EntityCollection[UnifiedRoleManagementPolicyRule](
                self.context, UnifiedRoleManagementPolicyRule, ResourcePath("rules", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedRoleManagementPolicy"
