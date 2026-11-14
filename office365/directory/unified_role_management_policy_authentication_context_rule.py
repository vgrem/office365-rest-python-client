from __future__ import annotations

from typing import Optional

from office365.directory.unified_role_management_policy_rule import UnifiedRoleManagementPolicyRule
from office365.runtime.types.odata_property import odata


class UnifiedRoleManagementPolicyAuthenticationContextRule(UnifiedRoleManagementPolicyRule):
    @odata(name="claimValue")
    @property
    def claim_value(self) -> Optional[str]:
        """Gets the claimValue property"""
        return self.properties.get("claimValue", None)

    @odata(name="isEnabled")
    @property
    def is_enabled(self) -> Optional[bool]:
        """Gets the isEnabled property"""
        return self.properties.get("isEnabled", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedRoleManagementPolicyAuthenticationContextRule"
