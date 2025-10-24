from enum import Enum


class CallTranscriptionState(Enum):
    notStarted = "0"
    active = "1"
    inactive = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CallTranscriptionState"
