from __future__ import annotations

from dataclasses import field

from office365.directory.policies.crosstenant.target_configuration import (
    CrossTenantAccessPolicyTargetConfiguration,
)
from office365.runtime.client_value import ClientValue


class CrossTenantAccessPolicyM365CollaborationInboundSetting(ClientValue):
    users: CrossTenantAccessPolicyTargetConfiguration = field(default_factory=CrossTenantAccessPolicyTargetConfiguration)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantAccessPolicyM365CollaborationInboundSetting"
