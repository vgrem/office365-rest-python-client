from enum import Enum


class ProvisioningStatusErrorCategory(Enum):
    failure = "0"
    nonServiceFailure = "1"
    success = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisioningStatusErrorCategory"
