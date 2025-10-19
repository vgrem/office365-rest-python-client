from enum import Enum


class RemindBeforeTimeInMinutesType(Enum):
    mins15 = "0"
    unknownFutureValue = "100"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RemindBeforeTimeInMinutesType"
