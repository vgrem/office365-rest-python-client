from enum import Enum


class BrowserSharedCookieSourceEnvironment(Enum):
    microsoftEdge = "0"
    internetExplorer11 = "1"
    both = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BrowserSharedCookieSourceEnvironment"
