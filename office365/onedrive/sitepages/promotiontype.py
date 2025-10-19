from enum import Enum


class PagePromotionType(Enum):
    microsoftReserved = "0"
    page = "1"
    newsPost = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PagePromotionType"
