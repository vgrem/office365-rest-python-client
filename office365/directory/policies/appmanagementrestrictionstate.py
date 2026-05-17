from enum import Enum


class AppManagementRestrictionState(Enum):
    enabled = "1"
    disabled = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AppManagementRestrictionState"
