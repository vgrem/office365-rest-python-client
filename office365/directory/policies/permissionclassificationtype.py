from enum import Enum


class PermissionClassificationType(Enum):
    low = "1"
    medium = "2"
    high = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PermissionClassificationType"
