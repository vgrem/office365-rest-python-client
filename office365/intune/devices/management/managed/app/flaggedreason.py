from enum import Enum


class ManagedAppFlaggedReason(Enum):
    none = "0"
    rootedDevice = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ManagedAppFlaggedReason"
