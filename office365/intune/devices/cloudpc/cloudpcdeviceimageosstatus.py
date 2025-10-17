from enum import Enum


class CloudPcDeviceImageOsStatus(Enum):
    supported = "0"
    supportedWithWarning = "1"
    unknown = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcDeviceImageOsStatus"
