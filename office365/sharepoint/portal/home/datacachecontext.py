from office365.runtime.client_value import ClientValue


class SharePointHomeDataCacheContext(ClientValue):

    def __init__(
        self,
        cache_key: str = None,
        hash_: str = None,
        list_item_id: int = None,
        my_site_url: str = None,
        time: str = None,
        version: str = None,
    ):
        self.CacheKey = cache_key
        self.Hash = hash_
        self.ListItemId = list_item_id
        self.MySiteUrl = my_site_url
        self.Time = time
        self.Version = version
