from typing import Optional

from office365.runtime.client_value import ClientValue


class TranslationNotificationRecipient(ClientValue):
    def __init__(self, login_name: Optional[str] = None):
        self.LoginName = login_name
