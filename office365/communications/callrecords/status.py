from enum import Enum


class CallRecordingStatus(Enum):
    success = "0"
    failure = "1"
    initial = "2"
    chunkFinished = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CallRecordingStatus"
