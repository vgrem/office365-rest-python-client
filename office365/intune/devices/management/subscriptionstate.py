from enum import Enum


class DeviceManagementSubscriptionState(Enum):
    pending = "0"
    active = "1"
    warning = "2"
    disabled = "3"
    deleted = "4"
    blocked = "5"
    lockedOut = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceManagementSubscriptionState"
