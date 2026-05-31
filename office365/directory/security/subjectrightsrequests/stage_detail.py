from office365.directory.privacy.subjectrightsrequeststage import SubjectRightsRequestStage
from office365.directory.privacy.subjectrightsrequeststagestatus import SubjectRightsRequestStageStatus
from office365.runtime.client_value import ClientValue


class SubjectRightsRequestStageDetail(ClientValue):
    stage: SubjectRightsRequestStage = SubjectRightsRequestStage.contentRetrieval
    status: SubjectRightsRequestStageStatus = SubjectRightsRequestStageStatus.notStarted
    "Represents the properties of the stages of a subject rights request."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SubjectRightsRequestStageDetail"
