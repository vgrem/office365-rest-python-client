from enum import Enum


class UnifiedRoleScheduleRequestActions(Enum):
    adminAssign = "1"
    adminUpdate = "2"
    adminRemove = "3"
    selfActivate = "4"
    selfDeactivate = "5"
    adminExtend = "6"
    adminRenew = "7"
    selfExtend = "8"
    selfRenew = "9"
    unknownFutureValue = "10"

    @property
    def entity_type_name(self):
        return "microsoft.graph.UnifiedRoleScheduleRequestActions"
