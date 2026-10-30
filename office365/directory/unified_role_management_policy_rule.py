from __future__ import annotations

from office365.directory.unified_role_management_policy_rule_target import UnifiedRoleManagementPolicyRuleTarget
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UnifiedRoleManagementPolicyRule(Entity):
    @odata(name="target")
    @property
    def target(self) -> UnifiedRoleManagementPolicyRuleTarget:
        """Gets the target property"""
        return self.properties.get("target", UnifiedRoleManagementPolicyRuleTarget())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedRoleManagementPolicyRule"
