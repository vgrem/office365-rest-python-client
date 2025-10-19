from enum import Enum


class ConditionalAccessClientApp(Enum):
    all = "0"
    browser = "1"
    mobileAppsAndDesktopClients = "2"
    exchangeActiveSync = "3"
    easSupported = "4"
    other = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ConditionalAccessClientApp"
