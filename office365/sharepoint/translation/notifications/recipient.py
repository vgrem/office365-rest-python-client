from typing import Optional

from office365.runtime.client_value import ClientValue


class TranslationNotificationRecipient(ClientValue):
    LoginName: Optional[str] = None
