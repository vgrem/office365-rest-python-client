from enum import Enum


class AutomaticRepliesStatus(Enum):
    disabled = "0"
    alwaysEnabled = "1"
    scheduled = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AutomaticRepliesStatus"
