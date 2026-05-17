from enum import Enum


class SubjectRightsRequestStage(Enum):
    contentRetrieval = "0"
    contentReview = "1"
    generateReport = "2"
    contentDeletion = "3"
    caseResolved = "4"
    contentEstimate = "5"
    unknownFutureValue = "6"
    approval = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SubjectRightsRequestStage"
