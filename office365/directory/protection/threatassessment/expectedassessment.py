from enum import Enum


class ThreatExpectedAssessment(Enum):
    block = "1"
    unblock = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ThreatExpectedAssessment"
