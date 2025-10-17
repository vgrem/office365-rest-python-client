from enum import Enum


class DeviceComplianceActionType(Enum):
    noAction = "0"
    notification = "1"
    block = "2"
    retire = "3"
    wipe = "4"
    removeResourceAccessProfiles = "5"
    pushNotification = "9"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceComplianceActionType"
