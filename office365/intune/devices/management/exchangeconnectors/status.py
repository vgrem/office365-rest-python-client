from enum import Enum


class DeviceManagementExchangeConnectorStatus(Enum):
    none = "0"
    connectionPending = "1"
    connected = "2"
    disconnected = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceManagementExchangeConnectorStatus"
