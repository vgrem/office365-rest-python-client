from enum import Enum


class SectionEmphasisType(Enum):
    none = "0"
    neutral = "1"
    soft = "2"
    strong = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SectionEmphasisType"
