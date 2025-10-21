from enum import Enum


class TargetedManagedAppGroupType(Enum):
    selectedPublicApps = "0"
    allCoreMicrosoftApps = "1"
    allMicrosoftApps = "2"
    allApps = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TargetedManagedAppGroupType"
