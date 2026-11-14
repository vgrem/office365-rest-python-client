from __future__ import annotations

from dataclasses import field

from office365.directory.policies.crosstenant.b2_b_setting import CrossTenantAccessPolicyB2BSetting
from office365.directory.policies.devices_filter import DevicesFilter


class CrossTenantAccessPolicyTenantRestrictions(CrossTenantAccessPolicyB2BSetting):
    devices: DevicesFilter = field(default_factory=DevicesFilter)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantAccessPolicyTenantRestrictions"
