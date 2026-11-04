from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SharePointHomeDataCacheContext(ClientValue):
    CacheKey: Optional[str] = None
    Hash: Optional[str] = None
    ListItemId: Optional[int] = None
    MySiteUrl: Optional[str] = None
    Time: Optional[str] = None
    Version: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.Home.SharePointHomeDataCacheContext"
