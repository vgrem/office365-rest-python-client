from enum import Enum


class AppsUpdateChannelType(Enum):
    current = "0"
    monthlyEnterprise = "1"
    semiAnnual = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AppsUpdateChannelType"
