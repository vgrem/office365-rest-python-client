from __future__ import annotations

from enum import Enum


class DeviceAndAppManagementAssignmentFilterType(Enum):
    none = "0"
    include = "1"
    exclude = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceAndAppManagementAssignmentFilterType"
