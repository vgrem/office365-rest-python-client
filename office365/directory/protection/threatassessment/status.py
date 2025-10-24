from enum import Enum


class ThreatAssessmentStatus(Enum):
    pending = "1"
    completed = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ThreatAssessmentStatus"
