from enum import Enum


class ChatMessageImportance(Enum):
    normal = "0"
    high = "1"
    urgent = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ChatMessageImportance"
