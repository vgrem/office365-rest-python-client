from __future__ import annotations

from office365.directory.policies.crosstenant.accesspolicytargettype import CrossTenantAccessPolicyTargetType
from office365.runtime.client_value import ClientValue


class CrossTenantAccessPolicyTarget(ClientValue):
    target: str | None = None
    targetType: CrossTenantAccessPolicyTargetType = CrossTenantAccessPolicyTargetType.user

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantAccessPolicyTarget"
