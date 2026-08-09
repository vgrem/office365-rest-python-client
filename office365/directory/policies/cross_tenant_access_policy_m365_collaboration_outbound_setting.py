from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.cross_tenant_access_policy_target_configuration import (
    CrossTenantAccessPolicyTargetConfiguration,
)
from office365.runtime.client_value import ClientValue


@dataclass
class CrossTenantAccessPolicyM365CollaborationOutboundSetting(ClientValue):
    usersAndGroups: CrossTenantAccessPolicyTargetConfiguration = field(
        default_factory=CrossTenantAccessPolicyTargetConfiguration
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantAccessPolicyM365CollaborationOutboundSetting"
