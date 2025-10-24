from enum import Enum


class ThreatAssessmentContentType(Enum):
    mail = "1"
    url = "2"
    file = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ThreatAssessmentContentType"
