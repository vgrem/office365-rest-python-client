from enum import Enum


class ServiceUpdateSeverity(Enum):
    normal = "1"
    high = "2"
    critical = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ServiceUpdateSeverity"
