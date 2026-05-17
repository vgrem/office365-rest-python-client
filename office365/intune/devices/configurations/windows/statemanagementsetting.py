from enum import Enum


class StateManagementSetting(Enum):
    notConfigured = "0"
    blocked = "1"
    allowed = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.StateManagementSetting"
