from enum import Enum


class MicrosoftManagedDesktopType(Enum):
    notManaged = "0"
    premiumManaged = "1"
    standardManaged = "2"
    starterManaged = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MicrosoftManagedDesktopType"
