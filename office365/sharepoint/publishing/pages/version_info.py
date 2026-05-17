from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class SitePageVersionInfo(ClientValue):
    def __init__(self, last_version_created: Optional[datetime] = None, last_version_created_by: Optional[str] = None):
        """Represents the version information for a given SitePage."""
        self.LastVersionCreated = last_version_created
        self.LastVersionCreatedBy = last_version_created_by

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageVersionInfo"
