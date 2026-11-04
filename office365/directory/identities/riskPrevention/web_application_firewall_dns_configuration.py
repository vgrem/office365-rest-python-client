from __future__ import annotations

from office365.directory.identities.riskPrevention.web_application_firewall_dns_record_type import (
    WebApplicationFirewallDnsRecordType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class WebApplicationFirewallDnsConfiguration(ClientValue):
    isDomainVerified: bool | None = None
    isProxied: bool | None = None
    name: str | None = None
    recordType: WebApplicationFirewallDnsRecordType = WebApplicationFirewallDnsRecordType.cname
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebApplicationFirewallDnsConfiguration"
