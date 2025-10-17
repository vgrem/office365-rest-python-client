from enum import Enum


class DeviceHealthStatus(Enum):
    active = "0"
    inactive = "1"
    impairedCommunication = "2"
    noSensorData = "3"
    noSensorDataImpairedCommunication = "4"
    unknown = "5"
    unknownFutureValue = "31"

    @property
    def entity_type_name(self):
        return "microsoft.graph.security.DeviceHealthStatus"
