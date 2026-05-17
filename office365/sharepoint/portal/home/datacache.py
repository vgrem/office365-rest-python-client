from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.home.datacacheentry import SharePointHomeDataCacheEntry
from typing import Optional


class SharePointHomeDataCache(ClientValue):
    def __init__(self, key: Optional[str] = None, value: SharePointHomeDataCacheEntry = SharePointHomeDataCacheEntry()):
        self.Key = key
        self.Value = value

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.Home.SharePointHomeDataCache"
