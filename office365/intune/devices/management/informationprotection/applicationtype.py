from enum import Enum


class ApplicationType(Enum):
    universal = "1"
    desktop = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ApplicationType"
