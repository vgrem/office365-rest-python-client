from office365.runtime.client_value import ClientValue


class TranslationNotificationRecipient(ClientValue):
    def __init__(self, login_name: str = None):
        self.LoginName = login_name
