from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identities.riskPrevention.web_application_firewall_dns_configuration import (
    WebApplicationFirewallDnsConfiguration,
)
from office365.runtime.client_value import ClientValue


@dataclass
class WebApplicationFirewallVerifiedDetails(ClientValue):
    dnsConfiguration: WebApplicationFirewallDnsConfiguration = field(
        default_factory=WebApplicationFirewallDnsConfiguration
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebApplicationFirewallVerifiedDetails"
