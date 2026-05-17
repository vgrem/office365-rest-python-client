from enum import Enum


class MediaSourceContentCategory(Enum):
    meeting = "0"
    liveStream = "1"
    presentation = "2"
    screenRecording = "3"
    story = "4"
    profile = "5"
    chat = "6"
    note = "7"
    comment = "8"
    unknownFutureValue = "9"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MediaSourceContentCategory"
