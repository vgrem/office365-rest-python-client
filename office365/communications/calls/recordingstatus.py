from enum import Enum


class RecordingStatus(Enum):
    unknown = "0"
    notRecording = "1"
    recording = "2"
    failed = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RecordingStatus"
