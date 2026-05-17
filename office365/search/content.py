from enum import Enum


class SearchContent(Enum):
    sharedContent = "1"
    privateContent = "2"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SearchContent"
