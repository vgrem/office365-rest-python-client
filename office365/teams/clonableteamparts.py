from enum import Enum


class ClonableTeamParts(Enum):
    apps = "1"
    tabs = "2"
    settings = "4"
    channels = "8"
    members = "16"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ClonableTeamParts"
