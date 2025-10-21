from enum import Enum


class VppTokenSyncStatus(Enum):
    none = "0"
    inProgress = "1"
    completed = "2"
    failed = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.VppTokenSyncStatus"
