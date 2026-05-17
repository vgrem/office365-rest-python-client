from enum import Enum


class Enablement(Enum):
    notConfigured = "0"
    enabled = "1"
    disabled = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Enablement"
