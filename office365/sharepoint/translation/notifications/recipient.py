from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class TranslationNotificationRecipient(ClientValue):
    LoginName: Optional[str] = None
