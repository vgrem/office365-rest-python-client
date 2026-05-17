from enum import Enum


class FilterMode(Enum):
    include = "0"
    exclude = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.FilterMode"
