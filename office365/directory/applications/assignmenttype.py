from enum import Enum


class AssignmentType(Enum):
    required = "0"
    recommended = "1"
    unknownFutureValue = "2"
    peerRecommended = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AssignmentType"
