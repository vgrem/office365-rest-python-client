from enum import Enum


class BrowserSiteMergeType(Enum):
    noMerge = "0"
    default = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BrowserSiteMergeType"
