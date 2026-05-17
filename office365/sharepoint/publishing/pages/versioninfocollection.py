from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class SitePageVersionInfoCollection(ClientValue):
    def __init__(self, created: Optional[datetime] = None, created_by: Optional[str] = None):
        self.Created = created
        self.CreatedBy = created_by

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageVersionInfoCollection"
