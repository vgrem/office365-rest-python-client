from enum import Enum


class Level(Enum):
    beginner = "0"
    intermediate = "1"
    advanced = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Level"
