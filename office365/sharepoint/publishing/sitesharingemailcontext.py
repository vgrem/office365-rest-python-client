from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SiteSharingEmailContext(ClientValue):
    CustomDescription: Optional[str] = None
    CustomTitle: Optional[str] = None
    Message: Optional[str] = None
    Url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SiteSharingEmailContext"
