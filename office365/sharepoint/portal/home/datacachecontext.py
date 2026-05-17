from office365.runtime.client_value import ClientValue
from typing import Optional


class SharePointHomeDataCacheContext(ClientValue):
    def __init__(
        self,
        cache_key: Optional[str] = None,
        hash_: Optional[str] = None,
        list_item_id: Optional[int] = None,
        my_site_url: Optional[str] = None,
        time: Optional[str] = None,
        version: Optional[str] = None,
    ):
        self.CacheKey = cache_key
        self.Hash = hash_
        self.ListItemId = list_item_id
        self.MySiteUrl = my_site_url
        self.Time = time
        self.Version = version

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.Home.SharePointHomeDataCacheContext"
