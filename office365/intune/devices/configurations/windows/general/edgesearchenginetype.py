from enum import Enum


class EdgeSearchEngineType(Enum):
    default = "0"
    bing = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EdgeSearchEngineType"
