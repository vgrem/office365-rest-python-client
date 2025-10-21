from enum import Enum


class ManagedBrowserType(Enum):
    notConfigured = "0"
    microsoftEdge = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ManagedBrowserType"
