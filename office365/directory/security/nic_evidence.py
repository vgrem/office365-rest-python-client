from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.ip_evidence import IpEvidence
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class NicEvidence(ClientValue):
    ipAddress: IpEvidence = field(default_factory=IpEvidence)
    macAddress: str | None = None
    vlans: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.NicEvidence"
