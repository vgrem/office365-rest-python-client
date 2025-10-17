from enum import Enum


class CloudPcProvisioningPolicyImageType(Enum):
    gallery = "0"
    custom = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcProvisioningPolicyImageType"
