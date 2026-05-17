from typing import Optional

from office365.runtime.client_value import ClientValue


class AnnouncementAuthor(ClientValue):
    def __init__(self, email: Optional[str] = None, id_: Optional[str] = None, name: Optional[str] = None):
        self.Email = email
        self.ID = id_
        self.Name = name

    @property
    def entity_type_name(self):
        return "SP.Publishing.AnnouncementAuthor"
