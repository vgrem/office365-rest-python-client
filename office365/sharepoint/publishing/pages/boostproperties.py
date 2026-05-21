from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SitePageBoostProperties(ClientValue):
    BoostOrder: Optional[float] = None
    BoostOrderVersion: Optional[int] = None
    BoostUntilExpiryDate: Optional[datetime] = None
    BoostUntilSeen: Optional[bool] = None
    BoostUntilUsersViewedCount: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageBoostProperties"
