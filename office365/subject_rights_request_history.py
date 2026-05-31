from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class SubjectRightsRequestHistory(ClientValue):
    changedBy: IdentitySet = field(default_factory=IdentitySet)
    eventDateTime: datetime = None
    stage: SubjectRightsRequestStage = SubjectRightsRequestStage.contentRetrieval
    stageStatus: SubjectRightsRequestStageStatus = SubjectRightsRequestStageStatus.notStarted
    type: str | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.SubjectRightsRequestHistory'