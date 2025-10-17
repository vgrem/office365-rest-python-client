from enum import Enum


class DeviceManagementPartnerTenantState(Enum):
    unknown = "0"
    unavailable = "1"
    enabled = "2"
    terminated = "3"
    rejected = "4"
    unresponsive = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceManagementPartnerTenantState"
