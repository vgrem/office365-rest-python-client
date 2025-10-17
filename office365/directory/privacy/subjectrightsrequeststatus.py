from enum import Enum


class SubjectRightsRequestStatus(Enum):
    active = "0"
    closed = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SubjectRightsRequestStatus"
