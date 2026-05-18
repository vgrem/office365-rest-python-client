from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.email_address import EmailAddress
from office365.outlook.mail.automaticreplies.mailtips import AutomaticRepliesMailTips
from office365.outlook.mail.tips.error import MailTipsError
from office365.runtime.client_value import ClientValue


@dataclass
class MailTips(ClientValue):
    """Informative messages about a recipient, displayed to users while they're composing a message.
    For example, an out-of-office message as an automatic reply for a message recipient.

    Fields:
        automaticReplies: Mail tips for automatic reply if set up by the recipient.
        customMailTip: A custom mail tip set on the recipient's mailbox.
        deliveryRestricted: Whether the recipient is delivery restricted.
        emailAddress: Email address of the recipient.
        error: Error raised when an error occurs during mail tips retrieval.
        externalMemberCount: Number of external members if the recipient is a distribution list.
        isModerated: Whether sending messages to the recipient requires approval.
    """

    automaticReplies: AutomaticRepliesMailTips = field(default_factory=AutomaticRepliesMailTips)
    customMailTip: str | None = None
    deliveryRestricted: bool | None = None
    emailAddress: EmailAddress = field(default_factory=EmailAddress)
    error: MailTipsError = field(default_factory=MailTipsError)
    externalMemberCount: int | None = None
    isModerated: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.mailTips"
