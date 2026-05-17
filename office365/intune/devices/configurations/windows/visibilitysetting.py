from enum import Enum


class VisibilitySetting(Enum):
    notConfigured = "0"
    hide = "1"
    show = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.VisibilitySetting"
