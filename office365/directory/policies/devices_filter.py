from __future__ import annotations

from dataclasses import dataclass

from office365.directory.policies.crosstenant.accesspolicytargetconfigurationaccesstype import (
    CrossTenantAccessPolicyTargetConfigurationAccessType,
)
from office365.runtime.client_value import ClientValue


@dataclass
class DevicesFilter(ClientValue):
    mode: CrossTenantAccessPolicyTargetConfigurationAccessType = (
        CrossTenantAccessPolicyTargetConfigurationAccessType.allowed
    )
    rule: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DevicesFilter"
