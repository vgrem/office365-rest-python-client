from __future__ import annotations

from enum import Enum


class DeviceAppManagementTaskCategory(Enum):
    unknown = "0"
    advancedThreatProtection = "1"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceAppManagementTaskCategory"
