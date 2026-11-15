from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.alerts.evidence.base import AlertEvidence
from office365.security.alerts.evidence.ip import IpEvidence


class DnsEvidence(AlertEvidence):
    domainName: str | None = None
    dnsServerIp: IpEvidence = field(default_factory=IpEvidence)
    hostIpAddress: IpEvidence = field(default_factory=IpEvidence)
    ipAddresses: ClientValueCollection[IpEvidence] = field(default_factory=lambda: ClientValueCollection(IpEvidence))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.DnsEvidence"
