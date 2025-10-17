from enum import Enum


class CloudPcProvisioningType(Enum):
    dedicated = "0"
    shared = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcProvisioningType"
