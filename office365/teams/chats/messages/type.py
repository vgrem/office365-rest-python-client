from enum import Enum


class ChatMessageType(Enum):
    message = "0"
    chatEvent = "1"
    typing = "2"
    unknownFutureValue = "3"
    systemEventMessage = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ChatMessageType"
