from enum import Enum


class BrowserSiteStatus(Enum):
    published = "0"
    pendingAdd = "1"
    pendingEdit = "2"
    pendingDelete = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BrowserSiteStatus"
