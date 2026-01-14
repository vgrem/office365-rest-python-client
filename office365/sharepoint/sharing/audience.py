from uuid import UUID

from office365.runtime.client_value import ClientValue


class Audience(ClientValue):
    def __init__(self, email: str = None, id_: UUID = None, title: str = None):
        self.email = email
        self.id = id_
        self.title = title
