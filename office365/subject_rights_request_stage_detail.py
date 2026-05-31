from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from office365.directory.privacy.subjectrightsrequeststage import SubjectRightsRequestStage
from office365.directory.privacy.subjectrightsrequeststagestatus import SubjectRightsRequestStageStatus

@dataclass
class SubjectRightsRequestStageDetail(ClientValue):
    error: PublicError = field(default_factory=PublicError)
    stage: SubjectRightsRequestStage = SubjectRightsRequestStage.contentRetrieval
    status: SubjectRightsRequestStageStatus = SubjectRightsRequestStageStatus.notStarted

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.SubjectRightsRequestStageDetail'