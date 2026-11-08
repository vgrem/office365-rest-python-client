from __future__ import annotations

from enum import Enum


class DeviceManagementComplianceActionType(Enum):
    noAction = "0"
    notification = "1"
    block = "2"
    retire = "3"
    wipe = "4"
    removeResourceAccessProfiles = "5"
    pushNotification = "9"
    remoteLock = "10"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementComplianceActionType"
