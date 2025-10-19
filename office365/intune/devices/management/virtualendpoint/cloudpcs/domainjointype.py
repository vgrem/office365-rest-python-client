from enum import Enum


class CloudPcDomainJoinType(Enum):
    azureADJoin = "0"
    hybridAzureADJoin = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcDomainJoinType"
