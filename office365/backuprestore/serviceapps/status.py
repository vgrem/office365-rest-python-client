from enum import Enum


class ServiceAppStatus(Enum):
    inactive = "0"
    active = "1"
    pendingActive = "2"
    pendingInactive = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ServiceAppStatus"
