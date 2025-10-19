from enum import Enum


class TitleAreaTextAlignmentType(Enum):
    left = "0"
    center = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TitleAreaTextAlignmentType"
