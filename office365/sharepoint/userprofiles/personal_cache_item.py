from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class PersonalCacheItem(ClientValue):
    """Object representing a PersonalCache item, returned from ReadCache methods of the PersonalCache."""

    AltTitle: Optional[str] = None
    CacheKey: Optional[str] = None
    CacheName: Optional[str] = None
    CacheValue: Optional[str] = None
    CacheValueHash: Optional[str] = None
    CacheValueHtml: Optional[str] = None
    CacheVersion: Optional[str] = None
    ContainerUrl: Optional[str] = None
    ListItemId: Optional[int] = None
    ListItemUniqueId: Optional[str] = None
    ModifiedTimeUtc: Optional[datetime] = None

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.PersonalCacheItem"
