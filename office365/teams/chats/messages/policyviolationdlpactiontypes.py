from enum import Enum


class ChatMessagePolicyViolationDlpActionTypes(Enum):
    none = "0"
    notifySender = "1"
    blockAccess = "2"
    blockAccessExternal = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ChatMessagePolicyViolationDlpActionTypes"
