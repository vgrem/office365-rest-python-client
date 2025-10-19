from enum import Enum


class PageLayoutType(Enum):
    microsoftReserved = "0"
    article = "1"
    home = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PageLayoutType"
