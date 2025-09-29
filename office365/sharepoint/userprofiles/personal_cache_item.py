from datetime import datetime

from office365.runtime.client_value import ClientValue


class PersonalCacheItem(ClientValue):

    def __init__(
        self,
        alt_title: str = None,
        cache_key: str = None,
        cache_name: str = None,
        cache_value: str = None,
        cache_value_hash: str = None,
        cache_value_html: str = None,
        cache_version: str = None,
        container_url: str = None,
        list_item_id: int = None,
        list_item_unique_id: str = None,
        modified_time_utc: datetime = None,
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
