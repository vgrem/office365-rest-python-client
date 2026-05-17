from typing import Optional

from office365.runtime.client_value import ClientValue


class RecipientLimitsInfo(ClientValue):
    def __init__(
        self,
        alias_only: Optional[int] = None,
        email_only: Optional[int] = None,
        mixed_recipients: Optional[int] = None,
        object_id_only: Optional[int] = None,
    ):
        self.alias_only = alias_only
        self.email_only = email_only
        self.mixed_recipients = mixed_recipients
        self.object_id_only = object_id_only
