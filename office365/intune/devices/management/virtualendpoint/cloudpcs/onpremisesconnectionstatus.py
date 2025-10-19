from enum import Enum


class CloudPcOnPremisesConnectionStatus(Enum):
    pending = "0"
    running = "1"
    passed = "2"
    failed = "3"
    warning = "4"
    informational = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcOnPremisesConnectionStatus"
