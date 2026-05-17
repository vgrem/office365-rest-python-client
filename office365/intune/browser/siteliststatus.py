from enum import Enum


class BrowserSiteListStatus(Enum):
    draft = "0"
    published = "1"
    pending = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BrowserSiteListStatus"
