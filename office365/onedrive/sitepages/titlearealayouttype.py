from enum import Enum


class TitleAreaLayoutType(Enum):
    imageAndTitle = "0"
    plain = "1"
    colorBlock = "2"
    overlap = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TitleAreaLayoutType"
