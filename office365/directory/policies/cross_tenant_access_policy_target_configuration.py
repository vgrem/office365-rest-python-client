from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.cross_tenant_access_policy_target import CrossTenantAccessPolicyTarget
from office365.directory.policies.crosstenant.accesspolicytargetconfigurationaccesstype import (
    CrossTenantAccessPolicyTargetConfigurationAccessType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class CrossTenantAccessPolicyTargetConfiguration(ClientValue):
    accessType: CrossTenantAccessPolicyTargetConfigurationAccessType = (
        CrossTenantAccessPolicyTargetConfigurationAccessType.allowed
    )
    targets: ClientValueCollection[CrossTenantAccessPolicyTarget] = field(
        default_factory=lambda: ClientValueCollection(CrossTenantAccessPolicyTarget)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantAccessPolicyTargetConfiguration"
