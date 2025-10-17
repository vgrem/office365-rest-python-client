from enum import Enum


class AccessPackageCatalogType(Enum):
    userManaged = "1"
    serviceDefault = "2"
    serviceManaged = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessPackageCatalogType"
