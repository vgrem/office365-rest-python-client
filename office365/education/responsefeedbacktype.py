from enum import Enum


class ResponseFeedbackType(Enum):
    none = "0"
    notDetected = "1"
    veryUnpleasant = "2"
    unpleasant = "3"
    neutral = "4"
    pleasant = "5"
    veryPleasant = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ResponseFeedbackType"
