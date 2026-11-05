from __future__ import annotations

from office365.directory.policies.crosstenant.accesspolicytargetconfigurationaccesstype import (
    CrossTenantAccessPolicyTargetConfigurationAccessType,
)
from office365.runtime.client_value import ClientValue


class DevicesFilter(ClientValue):
    mode: CrossTenantAccessPolicyTargetConfigurationAccessType = (
        CrossTenantAccessPolicyTargetConfigurationAccessType.allowed
    )
    rule: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DevicesFilter"
