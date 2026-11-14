from __future__ import annotations

from typing import Optional

from office365.directory.unified_role_management_policy_rule import UnifiedRoleManagementPolicyRule
from office365.runtime.types.duration import timedelta
from office365.runtime.types.odata_property import odata


class UnifiedRoleManagementPolicyExpirationRule(UnifiedRoleManagementPolicyRule):
    @odata(name="isExpirationRequired")
    @property
    def is_expiration_required(self) -> Optional[bool]:
        """Gets the isExpirationRequired property"""
        return self.properties.get("isExpirationRequired", None)

    @odata(name="maximumDuration")
    @property
    def maximum_duration(self) -> Optional[timedelta]:
        """Gets the maximumDuration property"""
        return self.properties.get("maximumDuration", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedRoleManagementPolicyExpirationRule"
