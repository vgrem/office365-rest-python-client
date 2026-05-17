from enum import Enum


class PostType(Enum):
    regular = "0"
    quick = "1"
    strategic = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PostType"
