from enum import Enum


class AndroidWorkProfileCrossProfileDataSharingType(Enum):
    deviceDefault = "0"
    preventAny = "1"
    allowPersonalToWork = "2"
    noRestrictions = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AndroidWorkProfileCrossProfileDataSharingType"
