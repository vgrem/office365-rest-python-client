from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.portal.home.datacache import SharePointHomeDataCache


@dataclass
class SharePointHomeDataCacheCollection(ClientValue):
    Items: ClientValueCollection[SharePointHomeDataCache] = field(
        default_factory=lambda: ClientValueCollection(SharePointHomeDataCache)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.Home.SharePointHomeDataCacheCollection"
