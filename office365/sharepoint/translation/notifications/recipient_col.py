from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.translation.notifications.recipient import (
    TranslationNotificationRecipient,
)


@dataclass
class TranslationNotificationRecipientCollection(ClientValue):
    LanguageCode: str | None = None
    Recipients: ClientValueCollection[TranslationNotificationRecipient] = field(
        default_factory=lambda: ClientValueCollection(TranslationNotificationRecipient)
    )
