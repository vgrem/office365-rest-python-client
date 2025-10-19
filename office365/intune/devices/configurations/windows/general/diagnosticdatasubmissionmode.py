from enum import Enum


class DiagnosticDataSubmissionMode(Enum):
    userDefined = "0"
    none = "1"
    basic = "2"
    enhanced = "3"
    full = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DiagnosticDataSubmissionMode"
