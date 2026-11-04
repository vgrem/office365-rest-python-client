from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.detonation_details import DetonationDetails
from office365.security.threat_type import ThreatType


@value
class AnalyzedEmailUrl(ClientValue):
    detectionMethod: str | None = None
    detonationDetails: DetonationDetails = field(default_factory=DetonationDetails)
    tenantAllowBlockListDetailInfo: str | None = None
    url: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AnalyzedEmailUrl"

    threatType: ThreatType = ThreatType.unknown
