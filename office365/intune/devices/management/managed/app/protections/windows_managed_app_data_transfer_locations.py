from __future__ import annotations

from enum import Enum


class WindowsManagedAppDataTransferLocations(Enum):
    none = "0"
    oneDriveForBusiness = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsManagedAppDataTransferLocations"
