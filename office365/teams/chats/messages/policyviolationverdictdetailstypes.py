from enum import Enum


class ChatMessagePolicyViolationVerdictDetailsTypes(Enum):
    none = "0"
    allowFalsePositiveOverride = "1"
    allowOverrideWithoutJustification = "2"
    allowOverrideWithJustification = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ChatMessagePolicyViolationVerdictDetailsTypes"
