from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.security.alerts.states.threat_type import ThreatType
from office365.security.attacksimulations.detonation_details import DetonationDetails


class AnalyzedEmailUrl(ClientValue):
    detectionMethod: str | None = None
    detonationDetails: DetonationDetails = field(default_factory=DetonationDetails)
    tenantAllowBlockListDetailInfo: str | None = None
    url: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AnalyzedEmailUrl"

    threatType: ThreatType = ThreatType.unknown
