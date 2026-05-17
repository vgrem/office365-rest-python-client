from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


class Audience(ClientValue):
    def __init__(self, email: Optional[str] = None, id_: Optional[UUID] = None, title: Optional[str] = None):
        self.email = email
        self.id = id_
        self.title = title
