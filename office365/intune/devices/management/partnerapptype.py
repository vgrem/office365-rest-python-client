from enum import Enum


class DeviceManagementPartnerAppType(Enum):
    unknown = "0"
    singleTenantApp = "1"
    multiTenantApp = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceManagementPartnerAppType"
