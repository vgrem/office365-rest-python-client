from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AnnouncementAuthor(ClientValue):
    Email: Optional[str] = None
    ID: Optional[str] = None
    Name: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.AnnouncementAuthor"
