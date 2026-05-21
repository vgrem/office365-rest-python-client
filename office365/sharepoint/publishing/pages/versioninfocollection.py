from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SitePageVersionInfoCollection(ClientValue):
    Created: Optional[datetime] = None
    CreatedBy: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageVersionInfoCollection"
