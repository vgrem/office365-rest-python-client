from enum import Enum


class EducationExternalSource(Enum):
    sis = "0"
    manual = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EducationExternalSource"
