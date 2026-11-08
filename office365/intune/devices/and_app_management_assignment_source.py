from __future__ import annotations

from enum import Enum


class DeviceAndAppManagementAssignmentSource(Enum):
    direct = "0"
    policySets = "1"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceAndAppManagementAssignmentSource"
