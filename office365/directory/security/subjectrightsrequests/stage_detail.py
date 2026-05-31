from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field

class SubjectRightsRequestStageDetail(ClientValue):
    error: PublicError = field(default_factory=PublicError)
    stage: SubjectRightsRequestStage = SubjectRightsRequestStage.contentRetrieval
    status: SubjectRightsRequestStageStatus = SubjectRightsRequestStageStatus.notStarted
    'Represents the properties of the stages of a subject rights request.'

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.SubjectRightsRequestStageDetail'