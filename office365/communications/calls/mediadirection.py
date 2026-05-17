from enum import Enum


class MediaDirection(Enum):
    inactive = "0"
    sendOnly = "1"
    receiveOnly = "2"
    sendReceive = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MediaDirection"
