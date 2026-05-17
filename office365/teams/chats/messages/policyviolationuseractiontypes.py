from enum import Enum


class ChatMessagePolicyViolationUserActionTypes(Enum):
    none = "0"
    override = "1"
    reportFalsePositive = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ChatMessagePolicyViolationUserActionTypes"
