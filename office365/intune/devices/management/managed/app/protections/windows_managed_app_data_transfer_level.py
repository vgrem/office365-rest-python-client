from __future__ import annotations

from enum import Enum


class WindowsManagedAppDataTransferLevel(Enum):
    allApps = "0"
    none = "1"
    selectedApps = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsManagedAppDataTransferLevel"
