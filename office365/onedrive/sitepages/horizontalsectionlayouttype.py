from enum import Enum


class HorizontalSectionLayoutType(Enum):
    none = "0"
    oneColumn = "1"
    twoColumns = "2"
    threeColumns = "3"
    oneThirdLeftColumn = "4"
    oneThirdRightColumn = "5"
    fullWidth = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.HorizontalSectionLayoutType"
