from enum import Enum


class CloudPcOnPremisesConnectionType(Enum):
    hybridAzureADJoin = "0"
    azureADJoin = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcOnPremisesConnectionType"
