from __future__ import annotations

from enum import Enum


class DeviceAppManagementTaskPriority(Enum):
    none = "0"
    high = "1"
    low = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceAppManagementTaskPriority"
