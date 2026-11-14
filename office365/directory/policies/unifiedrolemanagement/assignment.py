from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.policies.unifiedrolemanagement.policy import (
        UnifiedRoleManagementPolicy,
    )


class UnifiedRoleManagementPolicyAssignment(Entity):
    @odata(name="policyId")
    @property
    def policy_id(self) -> Optional[str]:
        """Gets the policyId property"""
        return self.properties.get("policyId", None)

    @odata(name="roleDefinitionId")
    @property
    def role_definition_id(self) -> Optional[str]:
        """Gets the roleDefinitionId property"""
        return self.properties.get("roleDefinitionId", None)

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

    @odata(name="policy", navigation=True)
    @property
    def policy(self) -> UnifiedRoleManagementPolicy:
        """Gets the policy property"""
        from office365.directory.policies.unifiedrolemanagement.policy import (
            UnifiedRoleManagementPolicy,
        )

        return self.properties.get(
            "policy", UnifiedRoleManagementPolicy(self.context, ResourcePath("policy", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedRoleManagementPolicyAssignment"
