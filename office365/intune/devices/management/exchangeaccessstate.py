from enum import Enum


class DeviceManagementExchangeAccessState(Enum):
    none = "0"
    unknown = "1"
    allowed = "2"
    blocked = "3"
    quarantined = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceManagementExchangeAccessState"
