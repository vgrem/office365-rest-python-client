from enum import Enum


class ManagedAppDataTransferLevel(Enum):
    allApps = "0"
    managedApps = "1"
    none = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ManagedAppDataTransferLevel"
