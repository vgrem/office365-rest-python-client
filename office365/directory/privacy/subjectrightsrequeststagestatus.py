from enum import Enum


class SubjectRightsRequestStageStatus(Enum):
    notStarted = "0"
    current = "1"
    completed = "3"
    failed = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SubjectRightsRequestStageStatus"
