from enum import Enum


class MediaState(Enum):
    active = "0"
    inactive = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MediaState"
