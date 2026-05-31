from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class WebApplicationFirewallDnsConfiguration(ClientValue):
    isDomainVerified: bool | None = None
    isProxied: bool | None = None
    name: str | None = None
    recordType: WebApplicationFirewallDnsRecordType = field(default_factory=WebApplicationFirewallDnsRecordType)
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.WebApplicationFirewallDnsConfiguration'