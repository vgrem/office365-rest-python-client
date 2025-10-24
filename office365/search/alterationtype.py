from enum import Enum


class SearchAlterationType(Enum):
    suggestion = "0"
    modification = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SearchAlterationType"
