from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.accessreview.notification_recipients_type import NotificationRecipientsType
from office365.directory.permissions.email_identity import EmailIdentity
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class NotificationRecipients(ClientValue):
    customRecipients: ClientValueCollection[EmailIdentity] = field(
        default_factory=lambda: ClientValueCollection(EmailIdentity)
    )
    role: NotificationRecipientsType = NotificationRecipientsType.none

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.NotificationRecipients"
