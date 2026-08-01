from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class DetonationDetails(ClientValue):
    analysisDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    detonationBehaviourDetailsV2: str | None = None
    detonationScreenshotUri: str | None = None
    detonationVerdict: str | None = None
    detonationVerdictReason: str | None = None
    entityMetadata: str | None = None
    mitreTechniques: str | None = None
    staticAnalysis: str | None = None
    submissionSource: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.DetonationDetails"
