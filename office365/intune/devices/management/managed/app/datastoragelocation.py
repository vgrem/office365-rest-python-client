from enum import Enum


class ManagedAppDataStorageLocation(Enum):
    oneDriveForBusiness = "1"
    sharePoint = "2"
    box = "3"
    localStorage = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ManagedAppDataStorageLocation"
