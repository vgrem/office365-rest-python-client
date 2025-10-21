from enum import Enum


class WindowsUpdateForBusinessUpdateWeeks(Enum):
    userDefined = "0"
    firstWeek = "1"
    secondWeek = "2"
    thirdWeek = "4"
    fourthWeek = "8"
    everyWeek = "15"
    unknownFutureValue = "22"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsUpdateForBusinessUpdateWeeks"
