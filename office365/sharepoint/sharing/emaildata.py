from typing import Optional

from office365.runtime.client_value import ClientValue


class EmailData(ClientValue):
    def __init__(self, body: Optional[str] = None, subject: Optional[str] = None):
        self.body = body
        self.subject = subject

    @property
    def entity_type_name(self):
        return "SP.Sharing.EmailData"
