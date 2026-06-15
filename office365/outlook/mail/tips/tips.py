from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.email_address import EmailAddress
from office365.outlook.mail.automaticreplies.mailtips import AutomaticRepliesMailTips
from office365.outlook.mail.recipient import Recipient
from office365.outlook.mail.recipientscopetype import RecipientScopeType
from office365.outlook.mail.tips.error import MailTipsError
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class MailTips(ClientValue):
    """Informative messages about a recipient, displayed to users while they're composing a message.
    For example, an out-of-office message as an automatic reply for a message recipient.
    """

    automaticReplies: AutomaticRepliesMailTips = field(default_factory=AutomaticRepliesMailTips)
    customMailTip: str | None = None
    deliveryRestricted: bool | None = None
    emailAddress: EmailAddress = field(default_factory=EmailAddress)
    error: MailTipsError = field(default_factory=MailTipsError)
    externalMemberCount: int | None = None
    isModerated: bool | None = None
    mailboxFull: bool | None = None
    maxMessageSize: int | None = None
    recipientScope: RecipientScopeType | None = None
    recipientSuggestions: ClientValueCollection[Recipient] = field(
        default_factory=lambda: ClientValueCollection(Recipient)
    )
    totalMemberCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.mailTips"
