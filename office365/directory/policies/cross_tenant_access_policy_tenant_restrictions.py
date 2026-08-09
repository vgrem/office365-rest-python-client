from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.devices_filter import DevicesFilter
from office365.runtime.client_value import ClientValue


@dataclass
class CrossTenantAccessPolicyTenantRestrictions(ClientValue):
    devices: DevicesFilter = field(default_factory=DevicesFilter)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantAccessPolicyTenantRestrictions"
