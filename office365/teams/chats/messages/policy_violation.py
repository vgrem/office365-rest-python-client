from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.teams.chats.messages.policy_violation_policy_tip import ChatMessagePolicyViolationPolicyTip
from office365.teams.chats.messages.policyviolationdlpactiontypes import ChatMessagePolicyViolationDlpActionTypes
from office365.teams.chats.messages.policyviolationuseractiontypes import ChatMessagePolicyViolationUserActionTypes
from office365.teams.chats.messages.policyviolationverdictdetailstypes import (
    ChatMessagePolicyViolationVerdictDetailsTypes,
)


@dataclass
class ChatMessagePolicyViolation(ClientValue):
    dlpAction: ChatMessagePolicyViolationDlpActionTypes = ChatMessagePolicyViolationDlpActionTypes.none
    justificationText: str | None = None
    policyTip: ChatMessagePolicyViolationPolicyTip = field(default_factory=ChatMessagePolicyViolationPolicyTip)
    userAction: ChatMessagePolicyViolationUserActionTypes = ChatMessagePolicyViolationUserActionTypes.none
    verdictDetails: ChatMessagePolicyViolationVerdictDetailsTypes = ChatMessagePolicyViolationVerdictDetailsTypes.none

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatMessagePolicyViolation"
