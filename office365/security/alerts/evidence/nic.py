from __future__ import annotations

from dataclasses import field

from office365.runtime.types.collections import StringCollection
from office365.security.alerts.evidence.base import AlertEvidence
from office365.security.alerts.evidence.ip import IpEvidence


class NicEvidence(AlertEvidence):
    ipAddress: IpEvidence = field(default_factory=IpEvidence)
    macAddress: str | None = None
    vlans: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.NicEvidence"
