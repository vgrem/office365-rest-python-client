from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.translation.notification_recipient import (
    TranslationNotificationRecipient,
)


class TranslationNotificationRecipientCollection(ClientValue):
    def __init__(self, language_code=None, recipients=None):
        """
        :param str language_code:
        :param list[str] recipients:
        """
        self.LanguageCode = language_code
        self.Recipients = ClientValueCollection(TranslationNotificationRecipient, recipients)
