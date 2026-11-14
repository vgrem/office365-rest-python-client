from __future__ import annotations

from office365.directory.policies.unifiedrolemanagement.rule import UnifiedRoleManagementPolicyRule
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class UnifiedRoleManagementPolicyEnablementRule(UnifiedRoleManagementPolicyRule):
    @odata(name="enabledRules")
    @property
    def enabled_rules(self) -> StringCollection:
        """Gets the enabledRules property"""
        return self.properties.get("enabledRules", StringCollection())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedRoleManagementPolicyEnablementRule"
