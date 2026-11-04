from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SitePageVersionInfoCollection(ClientValue):
    Created: Optional[datetime] = None
    CreatedBy: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageVersionInfoCollection"
