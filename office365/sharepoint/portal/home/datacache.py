from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.home.datacacheentry import SharePointHomeDataCacheEntry


@dataclass
class SharePointHomeDataCache(ClientValue):
    Key: Optional[str] = None
    Value: SharePointHomeDataCacheEntry = field(default_factory=SharePointHomeDataCacheEntry)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.Home.SharePointHomeDataCache"
