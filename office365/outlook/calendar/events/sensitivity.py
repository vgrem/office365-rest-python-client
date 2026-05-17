from enum import Enum


class Sensitivity(Enum):
    normal = "0"
    personal = "1"
    private = "2"
    confidential = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Sensitivity"
