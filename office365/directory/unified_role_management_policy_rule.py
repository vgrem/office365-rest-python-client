from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.unified_role_management_policy_rule_target import (
        UnifiedRoleManagementPolicyRuleTarget,
    )


class UnifiedRoleManagementPolicyRule(Entity):
    @odata(name="target")
    @property
    def target(self) -> UnifiedRoleManagementPolicyRuleTarget:
        """Gets the target property"""
        from office365.directory.unified_role_management_policy_rule_target import (
            UnifiedRoleManagementPolicyRuleTarget,
        )

        return self.properties.get("target", UnifiedRoleManagementPolicyRuleTarget())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedRoleManagementPolicyRule"
