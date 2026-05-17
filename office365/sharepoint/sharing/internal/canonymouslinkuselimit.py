from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class CAnonymousLinkUseLimit(ClientValue):
    def __init__(self, daily_limit_per_site: Optional[int] = None, expiration: Optional[datetime] = None):
        self.dailyLimitPerSite = daily_limit_per_site
        self.expiration = expiration

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Sharing.Internal.CAnonymousLinkUseLimit"
