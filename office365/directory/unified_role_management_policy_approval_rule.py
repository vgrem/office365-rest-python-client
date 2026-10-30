from __future__ import annotations

from office365.directory.approval_settings import ApprovalSettings
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UnifiedRoleManagementPolicyApprovalRule(Entity):
    @odata(name="setting")
    @property
    def setting(self) -> ApprovalSettings:
        """Gets the setting property"""
        return self.properties.get("setting", ApprovalSettings())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedRoleManagementPolicyApprovalRule"
