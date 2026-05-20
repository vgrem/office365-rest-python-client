from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.home.datacachecontext import (
    SharePointHomeDataCacheContext,
)


@dataclass
class SharePointHomeDataCacheEntry(ClientValue):
    CacheContext: SharePointHomeDataCacheContext = field(default_factory=SharePointHomeDataCacheContext)
    CacheValue: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.Home.SharePointHomeDataCacheEntry"
