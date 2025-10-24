from enum import Enum


class ServiceHealthClassificationType(Enum):
    """"""

    none = "0"
    unknownFutureValue = "3"
    advisory = "1"
    incident = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ServiceHealthClassificationType"
