from __future__ import annotations

from enum import Enum


class DeviceAppManagementTaskStatus(Enum):
    unknown = "0"
    pending = "1"
    active = "2"
    completed = "3"
    rejected = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceAppManagementTaskStatus"
