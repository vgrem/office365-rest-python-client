from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SitePageVersionInfo(ClientValue):
    """Represents the version information for a given SitePage."""

    LastVersionCreated: Optional[datetime] = None
    LastVersionCreatedBy: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageVersionInfo"
