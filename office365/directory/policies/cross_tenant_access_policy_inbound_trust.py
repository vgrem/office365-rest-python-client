from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CrossTenantAccessPolicyInboundTrust(ClientValue):
    isCompliantDeviceAccepted: bool | None = None
    isHybridAzureADJoinedDeviceAccepted: bool | None = None
    isMfaAccepted: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantAccessPolicyInboundTrust"
