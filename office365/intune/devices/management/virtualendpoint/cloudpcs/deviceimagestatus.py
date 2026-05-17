from enum import Enum


class CloudPcDeviceImageStatus(Enum):
    pending = "0"
    ready = "1"
    failed = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcDeviceImageStatus"
