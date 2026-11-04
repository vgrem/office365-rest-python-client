from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SitePageVersionInfo(ClientValue):
    """Represents the version information for a given SitePage."""

    LastVersionCreated: Optional[datetime] = None
    LastVersionCreatedBy: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageVersionInfo"
