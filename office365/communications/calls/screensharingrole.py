from enum import Enum


class ScreenSharingRole(Enum):
    viewer = "0"
    sharer = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ScreenSharingRole"
