from enum import Enum


class Modality(Enum):
    audio = "1"
    video = "2"
    videoBasedScreenSharing = "3"
    data = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Modality"

    screenSharing = "4"
