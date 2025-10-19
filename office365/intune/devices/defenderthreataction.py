from enum import Enum


class DefenderThreatAction(Enum):
    deviceDefault = "0"
    clean = "1"
    quarantine = "2"
    remove = "3"
    allow = "4"
    userDefined = "5"
    block = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DefenderThreatAction"
