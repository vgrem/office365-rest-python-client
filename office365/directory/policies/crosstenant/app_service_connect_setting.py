from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.crosstenant.target_configuration import (
    CrossTenantAccessPolicyTargetConfiguration,
)
from office365.runtime.client_value import ClientValue


@dataclass
class CrossTenantAccessPolicyAppServiceConnectSetting(ClientValue):
    applications: CrossTenantAccessPolicyTargetConfiguration = field(
        default_factory=CrossTenantAccessPolicyTargetConfiguration
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantAccessPolicyAppServiceConnectSetting"
