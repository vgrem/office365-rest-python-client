from enum import Enum


class ReadingCoachStoryType(Enum):
    aiGenerated = "0"
    readWorks = "1"
    userProvided = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ReadingCoachStoryType"
