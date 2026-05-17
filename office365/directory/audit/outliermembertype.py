from enum import Enum


class OutlierMemberType(Enum):
    user = "0"
    unknownFutureValue = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.OutlierMemberType"
