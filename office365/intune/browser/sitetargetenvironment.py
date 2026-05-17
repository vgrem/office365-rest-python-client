from enum import Enum


class BrowserSiteTargetEnvironment(Enum):
    internetExplorerMode = "0"
    internetExplorer11 = "1"
    microsoftEdge = "2"
    configurable = "3"
    none = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BrowserSiteTargetEnvironment"
