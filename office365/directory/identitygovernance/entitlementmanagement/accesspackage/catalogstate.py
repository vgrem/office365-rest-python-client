from enum import Enum


class AccessPackageCatalogState(Enum):
    unpublished = "1"
    published = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessPackageCatalogState"
