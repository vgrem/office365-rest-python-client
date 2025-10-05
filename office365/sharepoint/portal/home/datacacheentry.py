from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.home.datacachecontext import (
    SharePointHomeDataCacheContext,
)


class SharePointHomeDataCacheEntry(ClientValue):

    def __init__(
        self,
        cache_context: SharePointHomeDataCacheContext = SharePointHomeDataCacheContext(),
        cache_value: str = None,
    ):
        self.CacheContext = cache_context
        self.CacheValue = cache_value
