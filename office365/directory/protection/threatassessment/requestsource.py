from enum import Enum


class ThreatAssessmentRequestSource(Enum):
    undefined = "0"
    user = "1"
    administrator = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ThreatAssessmentRequestSource"
