from enum import Enum


class DeviceManagementExchangeConnectorSyncType(Enum):
    fullSync = "0"
    deltaSync = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceManagementExchangeConnectorSyncType"
