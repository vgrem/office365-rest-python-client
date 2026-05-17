from enum import Enum


class ThreatAssessmentResultType(Enum):
    checkPolicy = "1"
    rescan = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ThreatAssessmentResultType"
