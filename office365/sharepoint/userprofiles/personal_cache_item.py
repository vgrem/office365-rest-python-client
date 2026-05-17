from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class PersonalCacheItem(ClientValue):
    def __init__(
        self,
        alt_title: Optional[str] = None,
        cache_key: Optional[str] = None,
        cache_name: Optional[str] = None,
        cache_value: Optional[str] = None,
        cache_value_hash: Optional[str] = None,
        cache_value_html: Optional[str] = None,
        cache_version: Optional[str] = None,
        container_url: Optional[str] = None,
        list_item_id: Optional[int] = None,
        list_item_unique_id: Optional[str] = None,
        modified_time_utc: Optional[datetime] = None,
    ):
        """Object representing a PersonalCache item, returned from ReadCache methods of the PersonalCache."""
        self.AltTitle = alt_title
        self.CacheKey = cache_key
        self.CacheName = cache_name
        self.CacheValue = cache_value
        self.CacheValueHash = cache_value_hash
        self.CacheValueHtml = cache_value_html
        self.CacheVersion = cache_version
        self.ContainerUrl = container_url
        self.ListItemId = list_item_id
        self.ListItemUniqueId = list_item_unique_id
        self.ModifiedTimeUtc = modified_time_utc

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.PersonalCacheItem"
