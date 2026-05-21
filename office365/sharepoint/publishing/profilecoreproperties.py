from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ProfileCoreProperties(ClientValue):
    PictureUrl: Optional[str] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfileCoreProperties"
