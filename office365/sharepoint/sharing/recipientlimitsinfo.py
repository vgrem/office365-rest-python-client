from office365.runtime.client_value import ClientValue


class RecipientLimitsInfo(ClientValue):

    def __init__(
        self,
        alias_only: int = None,
        email_only: int = None,
        mixed_recipients: int = None,
        object_id_only: int = None,
    ):
        self.alias_only = alias_only
        self.email_only = email_only
        self.mixed_recipients = mixed_recipients
        self.object_id_only = object_id_only
