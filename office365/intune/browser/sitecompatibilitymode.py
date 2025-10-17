from enum import Enum


class BrowserSiteCompatibilityMode(Enum):
    default = "0"
    internetExplorer8Enterprise = "1"
    internetExplorer7Enterprise = "2"
    internetExplorer11 = "3"
    internetExplorer10 = "4"
    internetExplorer9 = "5"
    internetExplorer8 = "6"
    internetExplorer7 = "7"
    internetExplorer5 = "8"
    unknownFutureValue = "9"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BrowserSiteCompatibilityMode"
