from enum import Enum


class ProvisioningResult(Enum):
    success = "0"
    failure = "1"
    skipped = "2"
    warning = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisioningResult"
