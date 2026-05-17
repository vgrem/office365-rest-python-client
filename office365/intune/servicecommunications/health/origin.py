from enum import Enum


class ServiceHealthOrigin(Enum):
    microsoft = "1"
    thirdParty = "2"
    customer = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ServiceHealthOrigin"
