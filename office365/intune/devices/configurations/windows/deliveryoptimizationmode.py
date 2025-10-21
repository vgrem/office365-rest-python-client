from enum import Enum


class WindowsDeliveryOptimizationMode(Enum):
    userDefined = "0"
    httpOnly = "1"
    httpWithPeeringNat = "2"
    httpWithPeeringPrivateGroup = "3"
    httpWithInternetPeering = "4"
    simpleDownload = "99"
    bypassMode = "100"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsDeliveryOptimizationMode"
