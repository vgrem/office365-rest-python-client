from enum import Enum


class Importance(Enum):
    """The importance of the message"""

    low = "low"
    normal = "normal"
    high = "high"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Importance"
