from office365.directory.privacy.subjectrightsrequeststage import SubjectRightsRequestStage
from office365.directory.privacy.subjectrightsrequeststagestatus import SubjectRightsRequestStageStatus
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from office365.directory.privacy.subjectrightsrequeststage import SubjectRightsRequestStage
from office365.directory.privacy.subjectrightsrequeststagestatus import SubjectRightsRequestStageStatus

class SubjectRightsRequestStageDetail(ClientValue):
    stage: SubjectRightsRequestStage = SubjectRightsRequestStage.contentRetrieval
    status: SubjectRightsRequestStageStatus = SubjectRightsRequestStageStatus.notStarted
    error: PublicError = field(default_factory=PublicError)
    'Represents the properties of the stages of a subject rights request.'

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.SubjectRightsRequestStageDetail'