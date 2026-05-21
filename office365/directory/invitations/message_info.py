from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.mail.recipient import Recipient
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class InvitedUserMessageInfo(ClientValue):
    """The invitedUserMessageInfo object allows you to configure the invitation message."""

    ccRecipients: ClientValueCollection[Recipient] = field(default_factory=lambda: ClientValueCollection(Recipient))
    customizedMessageBody: str | None = None
    messageLanguage: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.InvitedUserMessageInfo"
