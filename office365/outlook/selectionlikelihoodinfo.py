from enum import Enum


class SelectionLikelihoodInfo(Enum):
    notSpecified = "0"
    high = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SelectionLikelihoodInfo"
