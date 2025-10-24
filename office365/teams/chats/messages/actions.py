from enum import Enum


class ChatMessageActions(Enum):
    reactionAdded = "1"
    reactionRemoved = "2"
    actionUndefined = "4"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ChatMessageActions"
