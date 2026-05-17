from enum import Enum


class OutlierContainerType(Enum):
    group = "0"
    unknownFutureValue = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.OutlierContainerType"
