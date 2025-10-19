from enum import Enum


class SiteArchiveStatus(Enum):
    recentlyArchived = "0"
    fullyArchived = "1"
    reactivating = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SiteArchiveStatus"
