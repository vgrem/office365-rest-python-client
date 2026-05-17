from enum import Enum


class WellknownListName(Enum):
    none = "0"
    defaultList = "1"
    flaggedEmails = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WellknownListName"
