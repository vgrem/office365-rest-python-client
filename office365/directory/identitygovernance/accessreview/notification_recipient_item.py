from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.accessreview.notification_recipient_scope import (
    AccessReviewNotificationRecipientScope,
)
from office365.runtime.client_value import ClientValue


@dataclass
class AccessReviewNotificationRecipientItem(ClientValue):
    notificationRecipientScope: AccessReviewNotificationRecipientScope = field(
        default_factory=AccessReviewNotificationRecipientScope
    )
    notificationTemplateType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewNotificationRecipientItem"
