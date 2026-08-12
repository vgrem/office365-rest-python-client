from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.events.sensitivity import Sensitivity
from office365.outlook.mail.messages.actionflag import MessageActionFlag
from office365.outlook.mail.messages.rules.size_range import SizeRange
from office365.outlook.mail.recipient import Recipient
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


@dataclass
class MessageRulePredicates(ClientValue):
    """Represents the set of conditions and exceptions that are available for a rule."""

    bodyContains: StringCollection = field(default_factory=StringCollection)
    bodyOrSubjectContains: StringCollection = field(default_factory=StringCollection)
    categories: StringCollection = field(default_factory=StringCollection)
    fromAddresses: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(Recipient))
    hasAttachments: bool | None = None
    headerContains: StringCollection = field(default_factory=StringCollection)
    importance: str | None = None
    isApprovalRequest: bool | None = None
    isAutomaticForward: bool | None = None
    isAutomaticReply: bool | None = None
    isEncrypted: bool | None = None
    isMeetingRequest: bool | None = None
    isMeetingResponse: bool | None = None
    isNonDeliveryReport: bool | None = None
    isPermissionControlled: bool | None = None
    isReadReceipt: bool | None = None
    isSigned: bool | None = None
    isVoicemail: bool | None = None
    messageActionFlag: MessageActionFlag = MessageActionFlag.any
    notSentToMe: bool | None = None
    recipientContains: StringCollection = field(default_factory=StringCollection)
    senderContains: StringCollection = field(default_factory=StringCollection)
    sensitivity: Sensitivity = Sensitivity.normal
    sentCcMe: bool | None = None
    sentOnlyToMe: bool | None = None
    sentToAddresses: ClientValueCollection[Recipient] = field(default_factory=lambda: ClientValueCollection(Recipient))
    sentToMe: bool | None = None
    sentToOrCcMe: bool | None = None
    subjectContains: StringCollection = field(default_factory=StringCollection)
    withinSizeRange: SizeRange = field(default_factory=SizeRange)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MessageRulePredicates"
