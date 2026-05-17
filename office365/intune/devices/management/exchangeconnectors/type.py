from enum import Enum


class DeviceManagementExchangeConnectorType(Enum):
    onPremises = "0"
    hosted = "1"
    serviceToService = "2"
    dedicated = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceManagementExchangeConnectorType"
